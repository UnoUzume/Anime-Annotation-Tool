import cv2
from PIL import Image
import numpy as np
from concurrent.futures import ThreadPoolExecutor
import json
import base64
import zlib
import re
import io
import time
from pathlib import Path
from . import opencv1, opencv2
from .base import Patha

executor = ThreadPoolExecutor()


class Project:
    def __init__(self, annConf) -> None:
        self.videoFPath = Patha(annConf['videoPath'])
        self.videoStem = self.videoFPath.stem
        self.video1 = opencv1.Video(str(self.videoFPath))
        self.video2 = opencv2.Video(str(self.videoFPath))
        self.video1.keyframes = self.video2.keyframes

        self.annDPath: Path = Patha('annotation').joinpath(self.videoStem)
        self.annDPath.mkdir(parents=True, exist_ok=True)

        with Patha(annConf['configDict'][self.videoStem]).open(encoding="UTF-8") as f:
            videoConf = json.load(f)

        self.labelList = videoConf["labelList"]
        lut_b = np.zeros(256, dtype=np.dtype('uint8'))
        lut_g = np.zeros(256, dtype=np.dtype('uint8'))
        lut_r = np.zeros(256, dtype=np.dtype('uint8'))
        for i in range(len(self.labelList)):
            label = self.labelList[i]
            label_id = int(label["id"])
            lut_b[label_id] = int(label["bgc"][4:6], 16)
            lut_g[label_id] = int(label["bgc"][2:4], 16)
            lut_r[label_id] = int(label["bgc"][0:2], 16)
        self.lut = np.dstack((lut_b, lut_g, lut_r))

        self.frameNum_gj = 0  # frame_num_get_just
        # self.mask_water_dic = {}  # compressed

    def savePic(self, picname, pic):
        filename = self.annDPath.joinpath(str(self.frameNum_gj)+picname)
        cv2.imwrite(str(filename), pic, [cv2.IMWRITE_PNG_COMPRESSION, 7])

    def saveMask(self, frame, maskImg, mWaterBGR, cWaterBGR):
        time_start = time.time()
        self.savePic("_frame.png", frame)
        self.savePic("_mCan.png", maskImg)
        self.savePic("_mWater.png", mWaterBGR)
        self.savePic("_cWater.png", cWaterBGR)
        time_end = time.time()
        print("save mask: "+str(time_end-time_start))

    def getframe0(self, frameNum, cCan_comped, mCan_comped):
        prevgray = cv2.cvtColor(self.video1.get(
            self.frameNum_gj), cv2.COLOR_BGR2GRAY)
        gray = cv2.cvtColor(self.video1.get(frameNum), cv2.COLOR_BGR2GRAY)
        self.frameNum_gj = frameNum
        cByte = zlib.decompress(cCan_comped)
        cImg: np.ndarray = np.frombuffer(
            cByte, dtype=np.uint8).copy().reshape(540, 960, 4)

        mByte = zlib.decompress(mCan_comped)
        mImg: np.ndarray = np.frombuffer(
            mByte, dtype=np.uint8).copy().reshape(540, 960, 4)
        # https://www.jb51.net/article/176131.htm
        # 使用Gunnar Farneback算法计算密集光流
        # shape:(540, 960, 2)
        flow = cv2.calcOpticalFlowFarneback(
            prevgray, gray, None, 0.5, 3, 15, 3, 7, 1.5, 0)
        y, x = np.mgrid[0:540, 0:960]
        y = np.clip((y-flow[..., 1]).astype(int), 0, 539)
        x = np.clip((x-flow[..., 0]).astype(int), 0, 959)
        cImg = cImg[y, x]
        mImg = mImg[y, x]
        cCan_comped = zlib.compress(cImg.tobytes())
        mCan_comped = zlib.compress(mImg.tobytes())
        return cCan_comped, mCan_comped

    def genWater(self, mCan_comped):
        maskByte = zlib.decompress(mCan_comped)
        maskImg: np.ndarray = np.frombuffer(
            maskByte[0::4], dtype=np.uint8).copy().reshape(540, 960)

        frame = self.video1.get(self.frameNum_gj)
        frame = cv2.resize(frame, (960, 540))

        mWaterImg: np.ndarray = cv2.watershed(
            frame, markers=maskImg.astype("int32"))
        mWaterImg = mWaterImg.astype("uint8")  # -1 -> 255
        mWaterBGR = cv2.cvtColor(mWaterImg, cv2.COLOR_GRAY2BGR)
        cWaterBGR = cv2.LUT(mWaterBGR, self.lut)
        cWaterRGBA = cv2.cvtColor(cWaterBGR, cv2.COLOR_BGR2RGBA)
        # executor.submit(self.saveMask, frame, maskImg, mWaterBGR, cWaterBGR)
        self.saveMask(frame, maskImg, mWaterBGR, cWaterBGR)
        cWater_comped = zlib.compress(cWaterRGBA.tobytes())
        return cWater_comped

    def getAttr(self, keys):
        result = {}
        print(keys)
        for key in keys:
            if key == 'keyframes':
                if self.video2.keyframes is not None:
                    result['keyframes'] = self.video2.keyframes.tolist()
            elif key == 'diffValue':
                if self.video2.diffValue is not None:
                    result['diffValue'] = self.video2.diffValue.tolist()
            elif key == 'diffValue_cut':
                if self.video2.diffValue is not None:
                    temp = self.video2.diffValue.copy()
                    temp[temp > 3e7] = 3e7
                    result['diffValue'] = temp.tolist()
            elif key == 'labelLUT':
                result['labelLUT'] = self.lut.tolist()
            elif key == 'labelList':
                result['labelList'] = self.labelList
        return result
