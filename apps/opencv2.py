import cv2
import os
import numpy as np
from threading import Thread
from multiprocessing import Process
from .base import Patha

# cv2.VideoCapture.get(0)	视频文件的当前位置（播放）以毫秒为单位
# cv2.VideoCapture.get(1)	基于以0开始的被捕获或解码的帧索引
# cv2.VideoCapture.get(2)	视频文件的相对位置（播放）：0=电影开始，1=影片的结尾。
# cv2.VideoCapture.get(3)	在视频流的帧的宽度
# cv2.VideoCapture.get(4)	在视频流的帧的高度
# cv2.VideoCapture.get(5)	帧速率
# cv2.VideoCapture.get(6)	编解码的4字-字符代码
# cv2.VideoCapture.get(7)	视频文件中的帧数


def nothing(x):
    pass


class Video:
    def __init__(self, path):
        self.cap= cv2.VideoCapture(path)
        self.filename = Patha(path).stem
        # https://www.it1352.com/1653431.html
        self.ana_keyframes_lock = 0
        self.frames_tatal = int(self.cap.get(7))
        self.keyframes = None
        self.diffValue = None
        if Patha("data/"+self.filename+" - keyframes.npy").exists():
            print("load keyframes.npy")
            self.keyframes = np.load(
                "data/"+self.filename+" - keyframes.npy")
            print("keyframes.shape:", self.keyframes.shape)
        if Patha("data/"+self.filename+" - diff_value.npy").exists():
            print("load diff_value.npy")
            self.diffValue = np.load(
                "data/"+self.filename+" - diff_value.npy")
            print("diff_value.shape:", self.diffValue.shape)

    def read_frames(self, n=1, is_loop=False):
        frames = []
        for _ in range(n):
            ret, frame = self.cap.read()
            if not ret:
                if is_loop:
                    self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame = self.cap.read()
                else:
                    return False, frames
            frames.append(frame)
        return True, frames

    def get(self, frame_num):
        print("frame_want: "+frame_num)
        frame_num = int(frame_num)
        frame_now = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
        print("frame_now: "+str(frame_now))
        if frame_now != frame_num:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
        ret, frame = self.cap.read()
        if not ret:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.cap.read()
        # total = self.cap0.get(7)
        _, img = cv2.imencode(".png", frame)
        img = img.tobytes()
        return img

    def ana_keyframes_process(self):
        self.keyframes = []
        self.diffValue = []

        print('ana_keyframes start')
        diff_value_pos_temp = []
        diff_value_sum_temp = []

        _, frame = self.cap.read()
        frame = cv2.resize(frame, (960, 540))
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (3, 3), 0)
        while 1:
            ret, frames = self.read_frames(3)
            if(not ret):
                break

            frame = cv2.resize(frames[2], (960, 540))
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (3, 3), 0)

            diff = cv2.absdiff(background, gray_frame)
            background = gray_frame
            diff_sum = np.sum(diff)
            pos = self.cap.get(cv2.CAP_PROP_POS_FRAMES)

            # if pos > 1000:
            #     break
            diff_value_pos_temp.append(pos)
            diff_value_sum_temp.append(diff_sum)

            if diff_sum > 1e7:
                self.keyframes.append(pos)
                self.ana_keyframes_lock = 1

        self.keyframes = np.array(self.keyframes)
        self.ana_keyframes_lock = 2
        diff_value_pos_temp = np.array(diff_value_pos_temp)
        diff_value_sum_temp = np.array(diff_value_sum_temp)
        self.diffValue = np.zeros(self.frames_tatal)
        self.diffValue[diff_value_pos_temp.astype(
            'int32').tolist()] = diff_value_sum_temp.astype('int32')
        print('ana_keyframes end')
        np.save("data/"+self.filename+" - keyframes", self.keyframes)
        np.save("data/"+self.filename+" - diff_value", self.diffValue)

    def ana_keyframes(self):
        print("启动开始")
        t = Process(target=self.ana_keyframes_process())
        t.start()
        print("启动完毕")
        return ""

    def get_keyframe_num(self, frame_str, frame_num_gj):
        if self.keyframes is None:
            return 0
        if frame_str == 'next':
            for index in range(len(self.keyframes)):
                if self.keyframes[index] > frame_num_gj:
                    return self.keyframes[index]
            return 0
        elif frame_str == 'pre':
            for index in range(len(self.keyframes)):
                if self.keyframes[index] > frame_num_gj-1:
                    return self.keyframes[index-1]
            return 0
