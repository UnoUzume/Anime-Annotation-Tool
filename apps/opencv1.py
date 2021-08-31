import cv2
import os
import numpy as np
from queue import Queue
from threading import Thread
from multiprocessing import Process
from concurrent.futures import ThreadPoolExecutor
from .base import Patha


def nothing(x):
    pass


class Video:
    def __init__(self, path):
        self.cap = cv2.VideoCapture(path)
        # https://www.it1352.com/1653431.html
        self.frame_cache = {}
        self.frame_num_cache = Queue(maxsize=100)
        self.keyframes = []
        self.frame_bytes_gj = 0
        self.get_frame_lock = 1
        self.executor = ThreadPoolExecutor()

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

    def getBytes(self, frame_num):
        frame = self.get(frame_num)
        # total = self.cap0.get(7)
        if frame is not None:
            _, img = cv2.imencode(".png", frame)
            img = img.tobytes()
            self.frame_bytes_gj = img
            return img
        else:
            return None

    def get(self, frame_num) -> np.ndarray:
        if frame_num in self.frame_cache:
            print("has cache")
            return self.frame_cache[frame_num]

        print("hasnot cache")
        if self.get_frame_lock == 1:
            self.get_frame_lock = 0
            frame_now = self.cap.get(cv2.CAP_PROP_POS_FRAMES)
            if frame_now != frame_num:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, frame_num)
            ret, frame = self.cap.read()
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = self.cap.read()
            self.get_frame_lock = 1

            frame = cv2.resize(frame, (960, 540))
            self.frame_cache[frame_num] = frame
            self.frame_num_cache.put(frame_num)
            self.executor.submit(self.do_frame_cache)
            return frame

        return None

    def do_frame_cache(self):
        if self.frame_num_cache.full():
            for _ in range(10):
                frame_num = self.frame_num_cache.get()
                del self.frame_cache[frame_num]

    def preGet(self, frame_num):
        for index in range(len(self.keyframes)):
            if self.keyframes[index] > frame_num:
                for i in range(10):
                    if not (self.keyframes[index+i] in self.frame_cache):
                        print("pre-get: "+str(self.keyframes[index+i]))
                        self.get(self.keyframes[index+i])
                return
