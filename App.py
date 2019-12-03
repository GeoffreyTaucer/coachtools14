from VideoOut import VidOut
from VidInput import Feed
from VidStorage import VidStorage
from threading import Thread
from time import time
import pygame as pg


class App:
    def __init__(self):
        self.vid_out = VidOut()
        self.vid_in = Feed()
        self.vid_storage = VidStorage(use_hard_drive=False)

        self.video_input_thread = Thread(target=self.video_in_loop)

        pg.init()
        pg.joystick.init()
        self.pad = pg.joystick.Joystick(0)
        self.pad.init()

        self.settings = {
            "version": "0.0.14",
            "feeding in": True,
            "shutting down": False,
            "displaying": "feed",
            "delay in seconds": 0,
            "delay in frames": 0,
            "display start": 0.0,
            "fetch id": 0,
        }

        print("")
        print("Thank you for using CoachTools 0.0.14 by Jeremy Waters")

    @property
    def delay_in_seconds(self):
        return self.settings["delay in seconds"]

    @delay_in_seconds.setter
    def delay_in_seconds(self, d: int):
        if d < 0:
            d = 0
        self.settings["delay in seconds"] = d
        self.settings["delay in frames"] = int(d * self.vid_in.fps)
        if self.settings["delay in frames"] > self.vid_storage.storage_limit:
            self.settings["delay in seconds"] = int(self.vid_storage.storage_limit/self.vid_in.fps)
            self.settings["delay in frames"] = int(self.settings["delay in seconds"] * self.vid_in.fps)
        self.settings["display start"] = time()

    @property
    def delay_in_frames(self):
        return self.settings["delay in frames"]

    @delay_in_frames.setter
    def delay_in_frames(self, d: int):
        if d < 0:
            d = 0
        elif d > self.vid_storage.storage_limit:
            d = self.vid_storage.storage_limit

        try:
            self.settings["delay in seconds"] = int(d/self.vid_in.fps)
        except ZeroDivisionError:
            self.settings["delay in seconds"] = 0

        self.settings["delay in frames"] = int(self.settings["delay in seconds"] * self.vid_in.fps)
        self.settings["display start"] = time()

    def video_in_loop(self):
        while not self.settings["shutting down"]:
            if self.settings["feeding in"]:
                frame = self.vid_in.get_frame()
                self.vid_storage.store_frame(frame)

    def shutdown(self):
        self.settings["shutting down"] = True
        self.video_input_thread.join()

    def handle_controller_input_main(self):
        for event in pg.event.get():
            if event.type == pg.JOYAXISMOTION:
                if self.pad.get_axis(0) > 0.5:
                    self.delay_in_seconds -= 1

                elif self.pad.get_axis(0) < -0.5:
                    self.delay_in_seconds += 1

            if event.type == pg.JOYBUTTONDOWN:
                if self.pad.get_button(9) == 1:
                    self.pause()

    def handle_controller_input_paused(self):
        for event in pg.event.get():
            if event.type == pg.JOYAXISMOTION:
                if self.pad.get_axis(0) > 0.5:
                    self.settings["fetch id"] -= int(self.vid_in.fps)

                elif self.pad.get_axis(0) < -0.5:
                    self.settings["fetch id"] += int(self.vid_in.fps)

                elif self.pad.get_axis(1) > 0.5:
                    self.settings["fetch id"] -= 1

                elif self.pad.get_axis(1) < -0.5:
                    self.settings["fetch id"] += 1

            elif event.type == pg.JOYBUTTONDOWN:
                if self.pad.get_button(9) == 1:
                    self.settings["feeding in"] = True
                    self.settings["displaying"] = "feed"

    def pause(self):
        self.settings["feeding in"] = False
        self.settings["displaying"] = "pause"
        self.settings["fetch id"] = self.delay_in_frames
        while self.settings["displaying"] == "pause":
            out_frame = self.vid_storage.fetch_frame(self.settings["fetch id"])
            k = self.vid_out.display_frame(out_frame)

            if k == ord('q'):
                self.shutdown()
                break

            self.handle_controller_input_paused()

    def main_func(self):
        self.delay_in_seconds = 3
        self.video_input_thread.start()
        while not self.settings["shutting down"]:
            out_frame = self.vid_storage.fetch_frame(self.delay_in_frames)
            if time() - self.settings["display start"] < 3:
                self.vid_out.add_overlay(out_frame, {"top left": f"{self.delay_in_seconds} seconds"})
            k = self.vid_out.display_frame(out_frame)
            if k == ord('q'):
                self.shutdown()
                break

            self.handle_controller_input_main()


if __name__ == '__main__':
    app = App()
    app.main_func()
