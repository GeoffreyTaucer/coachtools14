import os
import shutil
import cv2 as cv
import numpy as np
import atexit


class VidStorage:
    """
    Storage object for video frames.

    Attributes:
        use_hard_drive (bool):      If true, the hard drive will be used for storage (only recommended with SSD).
        path (string):              Relative directory in which to save video if hard drive is being used.
        storage_limit:              Maximum number of frames to be stored
    """

    def __init__(self, use_hard_drive=True, path='/vid', ssd_storage_limit=900, ram_storage_limit=300):
        self.use_hard_drive = use_hard_drive
        self.vid_box = []
        self.vid_path = f'{os.getcwd()}{path}'
        self.__storage_num = 0

        self.storage_limit = ssd_storage_limit if self.use_hard_drive else ram_storage_limit

        self.cleanup()
        atexit.register(self.cleanup)

    def store_frame(self, frame):
        if self.use_hard_drive:
            self.__store_on_hd(frame)

        else:
            self.__store_in_ram(frame)

    def __store_on_hd(self, frame):
        try:
            np.save(f'{self.vid_path}/{self.__storage_num}.npy', frame, allow_pickle=False)
            self.__storage_num += 1
            if self.__storage_num > self.storage_limit:
                self.__storage_num = 0

        except IOError:
            self.storage_limit = len(os.listdir(f'{self.vid_path}')) - 60
            print(f"Insufficient disk space. Storage limit decreased to {self.storage_limit} frames")

    def __store_in_ram(self, frame):
        try:
            self.vid_box.insert(0, frame)
            while len(self.vid_box) > self.storage_limit:
                self.vid_box.pop(-1)

        except MemoryError:
            self.storage_limit = len(self.vid_box) - 60
            print(f"Insufficient RAM. Storage limit decreased to {self.storage_limit} frames")

    def fetch_frame(self, delay_in_frames):
        if self.use_hard_drive:
            fetch_id = int(self.__storage_num - delay_in_frames -1)
            while fetch_id < 0:
                fetch_id += self.storage_limit
            if fetch_id > self.storage_limit:
                fetch_id = fetch_id % self.storage_limit

            try:
                return np.load(f'{self.vid_path}/{fetch_id}.npy')

            except FileNotFoundError:
                return None

        else:
            fetch_id = int(delay_in_frames)
            if fetch_id < 0:
                fetch_id = 0

            elif fetch_id >= self.storage_limit:
                fetch_id = self.storage_limit - 1

            try:
                return self.vid_box[fetch_id].copy()

            except IndexError:
                return None

    def cleanup(self):
        try:
            shutil.rmtree(self.vid_path)

        except FileNotFoundError:
            pass

        finally:
            os.mkdir(self.vid_path)
