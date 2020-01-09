print("Thank you for using CoachTools by Jeremy Waters")
print("Version 0.0.14")
print("Built using")
print("OpenCV and")

from VideoOut import VidOut
from VidInput import Feed
from VidStorage import VidStorage
from threading import Thread
from multiprocessing import Process
from playsound import playsound
from time import time
import pygame as pg


class App:
    def __init__(self):
        self.vid_out = VidOut()
        self.vid_in = Feed()
        self.vid_storage = VidStorage(use_hard_drive=True)

        self.video_input_thread = Thread(target=self.video_in_loop)

        self._settings = {
            "version": "0.0.14",
            "feeding in": True,
            "shutting down": False,
            "displaying": "feed",
            "delay in seconds": 0,
            "delay in frames": 0,
            "display start": 0.0,
            "fetch id": 0,
            "sleep after": 300 * self.vid_in.fps,
            "showing hold timer": False,
            "playing ding for hold": False,
            "already played ding": False,
            "hold goal": 0,
            "hold start": 0.0,
            "currently holding": False,
            "selected": 0,
        }

        pg.init()
        pg.joystick.init()
        self.pad = pg.joystick.Joystick(0)
        self.pad.init()

    @property
    def delay_in_seconds(self):
        return self._settings["delay in seconds"]

    @delay_in_seconds.setter
    def delay_in_seconds(self, d: int):
        if d < 0:
            d = 0
        self._settings["delay in seconds"] = d
        self._settings["delay in frames"] = int(d * self.vid_in.fps)
        if self._settings["delay in frames"] > self.vid_storage.storage_limit:
            self._settings["delay in seconds"] = int(self.vid_storage.storage_limit / self.vid_in.fps)
            self._settings["delay in frames"] = int(self._settings["delay in seconds"] * self.vid_in.fps)
        self._settings["display start"] = time()

    @property
    def delay_in_frames(self):
        return self._settings["delay in frames"]

    @delay_in_frames.setter
    def delay_in_frames(self, d: int):
        if d < 0:
            d = 0
        elif d > self.vid_storage.storage_limit:
            d = self.vid_storage.storage_limit

        try:
            self._settings["delay in seconds"] = int(d / self.vid_in.fps)
        except ZeroDivisionError:
            self._settings["delay in seconds"] = 0

        self._settings["delay in frames"] = int(self._settings["delay in seconds"] * self.vid_in.fps)
        self._settings["display start"] = time()

    def video_in_loop(self):
        while not self._settings["shutting down"]:
            if self._settings["feeding in"]:
                frame = self.vid_in.get_frame()

                if self._settings["showing hold timer"]:
                    if self.vid_in.motionless_frames == 3:
                        self._settings["hold start"] = time()
                        self._settings["currently holding"] = True

                    elif self.vid_in.motionless_frames > self.vid_in.fps:
                        held_time = round(time() - self._settings["hold start"], 1)
                        if self._settings["hold goal"] and held_time < self._settings["hold goal"]:
                            color = (0, 0, 255)
                            if self._settings["playing ding for hold"] and not self._settings["already played ding"]:
                                Process(target=self.play_ding).start()
                                self._settings["already played ding"] = True
                        else:
                            color = (0, 255, 0)
                        frame = self.vid_out.add_overlay(frame, {'bot left': [f"{held_time}"]}, color)

                    elif self.vid_in.motionless_frames == 0 and self._settings["currently holding"]:
                        self._settings["currently holding"] = False
                        self._settings["already played ding"] = False

                self.vid_storage.store_frame(frame)

    def shutdown(self):
        self._settings["shutting down"] = True
        self.video_input_thread.join()

    def handle_controller_input_main(self):
        for event in pg.event.get():
            if event.type == pg.JOYAXISMOTION:
                if self.pad.get_axis(1) > 0.5:
                    self.delay_in_seconds -= 1

                elif self.pad.get_axis(1) < -0.5:
                    self.delay_in_seconds += 1

            if event.type == pg.JOYBUTTONDOWN:
                if self.pad.get_button(9) == 1:
                    self.pause()

                elif self.pad.get_button(8) == 1:
                    self.menu()

    def handle_controller_input_paused(self):
        for event in pg.event.get():
            if event.type == pg.JOYAXISMOTION:
                if self.pad.get_axis(1) > 0.5:
                    self._settings["fetch id"] -= int(self.vid_in.fps)

                elif self.pad.get_axis(1) < -0.5:
                    self._settings["fetch id"] += int(self.vid_in.fps)

                elif self.pad.get_axis(0) > 0.5:
                    self._settings["fetch id"] -= 1

                elif self.pad.get_axis(0) < -0.5:
                    self._settings["fetch id"] += 1

            elif event.type == pg.JOYBUTTONDOWN:
                if self.pad.get_button(9) == 1:
                    self._settings["feeding in"] = True
                    self._settings["displaying"] = "feed"

    def handle_controller_input_menu(self):
        for event in pg.event.get():
            if event.type == pg.JOYAXISMOTION:
                if self.pad.get_axis(1) > 0.5:
                    self._settings["selected"] += 1
                    if self._settings["selected"] > 4:
                        self._settings["selected"] = 0

                elif self.pad.get_axis(1) < -0.5:
                    self._settings["selected"] -= 1
                    if self._settings["selected"] < 0:
                        self._settings["selected"] = 4

                elif self._settings["selected"] == 0:
                    if self.pad.get_axis(0) > 0.5:
                        self.delay_in_seconds += 1
                    elif self.pad.get_axis(0) < -0.5:
                        self.delay_in_seconds -= 1

                elif self._settings["selected"] == 1:
                    if self.pad.get_axis(0) > 0.5 or self.pad.get_axis(0) < -0.5:
                        self._settings["showing hold timer"] = not self._settings["showing hold timer"]

                elif self._settings["selected"] == 2:
                    if self.pad.get_axis(0) > 0.5:
                        self._settings["hold goal"] += 1
                    elif self.pad.get_axis(0) < -0.5:
                        self._settings["hold goal"] -= 1

                elif self._settings["selected"] == 3:
                    if self.pad.get_axis(0) > 0.5 or self.pad.get_axis(0) < -0.5:
                        self._settings["playing ding for hold"] = not self._settings["playing ding for hold"]

            elif self._settings["selected"] == 4 and event.type == pg.JOYBUTTONDOWN:
                self._settings["displaying"] = "feed"
                self._settings["display start"] = time()

    def pause(self):
        self._settings["feeding in"] = False
        self._settings["displaying"] = "pause"
        self._settings["fetch id"] = self.delay_in_frames
        while self._settings["displaying"] == "pause":
            out_frame = self.vid_storage.fetch_frame(self._settings["fetch id"])
            k = self.vid_out.display_frame(out_frame)

            if k == ord('q'):
                self.shutdown()
                break

            self.handle_controller_input_paused()

    def menu(self):
        self._settings["displaying"] = "menu"
        while self._settings["displaying"] == "menu":
            options = [
                f"{'-->' if self._settings['selected'] == 0 else '     '}Delay: <{self.delay_in_seconds}> seconds.",
                f"{'-->' if self._settings['selected'] == 1 else '     '}Hold timer: {'on' if self._settings['showing hold timer'] else 'off'}",
                f"{'-->' if self._settings['selected'] == 2 else '     '}    Hold goal: {self._settings['hold goal']} seconds",
                f"{'-->' if self._settings['selected'] == 3 else '     '}    Audio cue: {'on' if self._settings['playing ding for hold'] else 'off'}",
                f"{'-->' if self._settings['selected'] == 4 else '     '}Exit menu"
            ]
            blank = self.vid_out.get_blank()
            overlaid = self.vid_out.add_overlay(blank, {"top left": options,
                                                        "bot right": [f"Coach Tools version {self._settings['version']}"
                                                                      f" by Jeremy Waters"]})
            k = self.vid_out.display_frame(overlaid)
            if k == ord('q'):
                self.shutdown()
                break

            self.handle_controller_input_menu()

    @staticmethod
    def play_ding():
        try:
            playsound("ding.mp3")

        except FileNotFoundError:
            print(f"Oops! ding.mp3 not found!")

    def main_func(self):
        self.delay_in_seconds = 3
        self.video_input_thread.start()
        while not self._settings["shutting down"]:
            if self.vid_in.motionless_frames > self._settings["sleep after"]:
                self._settings["displaying"] = "blank"
            elif self.vid_in.motion_frames > 3:
                self._settings["displaying"] = "feed"

            if self._settings["displaying"] == "blank":
                out_frame = self.vid_out.get_blank()
                self._settings["display start"] = 0
            else:
                out_frame = self.vid_storage.fetch_frame(self.delay_in_frames)

            if time() - self._settings["display start"] < 3:
                out_frame = self.vid_out.add_overlay(out_frame, {'top left': [f"{self.delay_in_seconds} seconds"]})

            k = self.vid_out.display_frame(out_frame)
            if k == ord('q'):
                self.shutdown()
                break

            self.handle_controller_input_main()

        self.vid_in.cap.release()
        self.vid_storage.cleanup()


if __name__ == '__main__':
    app = App()
    app.main_func()
