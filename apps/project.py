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

        self.annDPath: Patha = Patha('annotation').joinpath(self.videoStem)
        self.annDPath.mkdir(parents=True, exist_ok=True)

        with Patha(annConf['configDict'][self.videoStem]).open(encoding="UTF-8") as f:
            videoConf = json.load(f)

        labelList = videoConf["labelList"]
        lut_b = np.zeros(256, dtype=np.dtype('uint8'))
        lut_g = np.zeros(256, dtype=np.dtype('uint8'))
        lut_r = np.zeros(256, dtype=np.dtype('uint8'))
        for i in range(len(labelList)):
            label = labelList[i]
            label_id = int(label["id"])
            lut_b[label_id] = int(label["bgc"][4:6], 16)
            lut_g[label_id] = int(label["bgc"][2:4], 16)
            lut_r[label_id] = int(label["bgc"][0:2], 16)
        self.lut = np.dstack((lut_b, lut_g, lut_r))

        self.frameNum_gj = 0  # frame_num_get_just
        # self.mask_water_dic = {}  # compressed

    def saveFile(self, filename, bytes):
        fo = open(self.annDPath.joinpath(filename), "wb")
        fo.write(bytes)
        fo.close()

    def saveMask(self, frame, maskImg, maskWater):
        time_start = time.time()
        _, png_data = cv2.imencode('.png', frame)
        self.saveFile(str(self.frameNum_gj)+"_frame.png", png_data)

        # self.saveFile(str(self.frameNum_gj) +
        #               "_mask_canvas.bytes", maskImg)

        maskWater = cv2.cvtColor(maskWater, cv2.COLOR_GRAY2RGB)
        _, png_data = cv2.imencode('.png', maskWater)
        self.saveFile(str(self.frameNum_gj)+"_mask_water.png", png_data)

        color_water = cv2.LUT(maskWater, self.lut)
        _, png_data = cv2.imencode('.png', color_water)
        self.saveFile(str(self.frameNum_gj)+"_color_water.png", png_data)
        time_end = time.time()
        print("save mask: "+str(time_end-time_start))

    def genWater(self, mCan_comped):
        maskByte = zlib.decompress(mCan_comped)
        maskImg: np.ndarray = np.frombuffer(
            maskByte[0::4], dtype=np.uint8).copy().reshape(540, 960)

        frame = self.video1.get(self.frameNum_gj)
        frame = cv2.resize(frame, (960, 540))

        maskWater: np.ndarray = cv2.watershed(
            frame, markers=maskImg.astype("int32"))
        maskWater = maskWater.astype("uint8")  # -1 -> 255

        maskWater_comped = zlib.compress(maskWater.tobytes())
        executor.submit(self.saveMask, frame, maskImg, maskWater)
        return maskWater_comped
