from VideoOut import VidOut
from VidInput import Feed
from VidStorage import VidStorage
from threading import Thread
from time import time
import pygame as pg


class App:
    def __init__(self):
        self.version = "0.0.14"
        self.vid_out = VidOut()
        self.vid_in = Feed()
        self.vid_storage = VidStorage(use_hard_drive=False)

        self.feeding_in = True
        self.display_status = "feed"
        self.shutting_down = False
        self.input_loop_thread = None

        self.hold_goal = None
        self.play_audio_cue = False

        self.delay_display_timer = None

        pg.init()
        pg.joystick.init()
        self.pad = pg.joystick.Joystick(0)
        self.pad.init()

        self.delay_in_seconds = None
        self.delay_in_frames = None
        self.fetch_id = None

        self.set_delay(3)

    def set_delay(self, delay_in_seconds):
        self.delay_in_seconds = delay_in_seconds
        if self.delay_in_seconds < 0:
            self.delay_in_seconds = 0
        self.delay_in_frames = delay_in_seconds * self.vid_in.fps
        if self.delay_in_frames > self.vid_storage.storage_limit:
            self.delay_in_seconds = int(self.vid_storage.storage_limit / self.vid_in.fps)
            self.delay_in_frames = self.delay_in_seconds * self.vid_in.fps
        self.delay_display_timer = time()

    def input_loop(self):
        while not self.shutting_down:
            if self.feeding_in:
                frame = self.vid_in.get_frame()
                self.vid_storage.store_frame(frame)

    def main(self):
        self.input_loop_thread = Thread(target=self.input_loop)
        self.input_loop_thread.start()
        self.delay_display_timer = time()
        while not self.shutting_down:
            if self.display_status == "feed":
                self.display_feed()

            elif self.display_status == "pause":
                self.pause()

    def display_feed(self):
        self.delay_in_frames = int(self.delay_in_seconds * self.vid_in.fps)
        frame = self.vid_storage.fetch_frame(self.delay_in_frames).copy()
        if time() - self.delay_display_timer < 3:
            self.vid_out.add_overlay(frame, {'top left': [f'Delay: {self.delay_in_seconds} sec']})
        k = self.show_frame(frame)

        if k == ord('q'):
            self.shut_down()

    def user_input_feed(self):
        for event in pg.event.get():
            if event.type == pg.JOYBUTTONDOWN:
                if self.pad.get_button(9) == 1:
                    self.feeding_in = False
                    self.fetch_id = self.delay_in_frames
                    self.display_status = "pause"

            elif event.type == pg.JOYAXISMOTION:
                if self.pad.get_axis(1) > 0.5:
                    self.set_delay(self.delay_in_seconds + 1)
                elif self.pad.get_axis(1) < -0.5:
                    self.set_delay(self.delay_in_seconds - 1)

                # elif self.pad.get_button(8) == 1:
                #     self.menu()

    def pause(self):
        frame = self.vid_storage.fetch_frame(self.fetch_id)
        k = self.show_frame(frame)

        if k == ord('q'):
            self.shut_down()

        self.user_input_pause()

    def user_input_pause(self):
        for event in pg.event.get():
            if event.type == pg.JOYAXISMOTION:
                if self.pad.get_axis(0) > 0.5:
                    self.fetch_id -= 1
                    if self.fetch_id < 0:
                        self.fetch_id = 0
                elif self.pad.get_axis(0) < -0.5:
                    self.fetch_id += 1
                    if self.fetch_id > self.vid_storage.storage_limit:
                        self.fetch_id = self.vid_storage.storage_limit

                elif self.pad.get_axis(1) > 0.5:
                    self.fetch_id -= int(self.vid_in.fps)
                    if self.fetch_id < 0:
                        self.fetch_id = 0
                elif self.pad.get_axis(1) < -0.5:
                    self.fetch_id += int(self.vid_in.fps)
                    if self.vid_in.fps >= self.vid_storage.storage_limit:
                        self.fetch_id = self.vid_storage.storage_limit

    def menu(self):  # unfinished
        self.display_status = "menu"
        selcted = 0
        while self.display_status == "menu":
            frame = self.vid_out.get_blank().copy()

    def show_frame(self, frame):
        out = frame.copy()
        if self.display_status == "feed" and self.delay_display_timer - time() < 3:
            self.vid_out.add_overlay(out, {"top left": [f"Delay set at {self.delay_in_seconds} sec"]})

        return self.vid_out.display_frame(out)

    def shut_down(self):
        self.display_status = "shutdown"
        self.vid_storage.cleanup()
        self.shutting_down = True
