import cv2 as cv
import numpy as np
from pyautogui import size


class VidOut:
    def __init__(self):
        self.width, self.height = size()
        self.out_window = "feed"

        cv.namedWindow(self.out_window, cv.WINDOW_GUI_NORMAL)
        cv.setWindowProperty(self.out_window, cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
        cv.setWindowProperty(self.out_window, cv.WND_PROP_ASPECT_RATIO, cv.WINDOW_KEEPRATIO)

    def get_blank(self):
        return np.zeros((self.height, self.width), np.uint8)

    def display_frame(self, frame):
        if frame is None:
            frame = self.get_blank()
            self.add_overlay(frame, {'bot right': ["Frame fetch failed"]})
        cv.imshow(self.out_window, frame)
        k = cv.waitKey(1) & 0xFF
        return k

    def add_overlay(self, frame, overlay_text, color=(200, 200, 0)):
        """
        Add overlay to a frame, return the frame

        overlay_text should be a dictionary. Key determines location, value should be a list containing lines of text
        to be displayed. Each list item will show on a separate line. There are currently no checks to prevent lines
        from being too long or too numerous.
        """
        corners = {
            'top left': self.__overlay_top_left,
            'top right': self.__overlay_top_right,
            'bot left': self.__overlay_bot_left,
            'bot right': self.__overlay_bot_right
        }
        if frame is None:
            frame = self.get_blank()
        overlaid = frame.copy()
        shape = overlaid.shape
        for key in overlay_text:
            try:
                overlaid = corners[key](overlaid, overlay_text[key], color, shape)

            except KeyError as e:
                print(f"Overlay failure: {e}")

        return overlaid

    @staticmethod
    def __overlay_top_left(frame, text_lines, color, _):
        x_orig = 10
        y_orig = 0
        for line in text_lines:
            text_width, text_height = cv.getTextSize(line, cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
            y_orig += text_height + 10
            cv.putText(frame, line, (x_orig, y_orig), cv.FONT_HERSHEY_SIMPLEX, 1, color, 1, lineType=cv.LINE_AA)
        return frame

    @staticmethod
    def __overlay_top_right(frame, text_lines, color, frame_shape):
        x_width = frame_shape[1]
        y_orig = 0

        for line in text_lines:
            text_width, text_height = cv.getTextSize(line, cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
            y_orig += text_height + 10
            x_orig = x_width - text_width - 10
            cv.putText(frame, line, (x_orig, y_orig), cv.FONT_HERSHEY_SIMPLEX, 1, color, 1, lineType=cv.LINE_AA)
        return frame

    @staticmethod
    def __overlay_bot_left(frame, text_lines, color, frame_shape):
        y_height, x_width = frame_shape[0], frame_shape[1]
        y_orig = y_height - ((cv.getTextSize(text_lines[0], cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0][1] + 10)
                             * len(text_lines)) + 20
        x_orig = 10

        for line in text_lines:
            text_width, text_height = cv.getTextSize(line, cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
            cv.putText(frame, line, (x_orig, y_orig), cv.FONT_HERSHEY_SIMPLEX, 1, color, 1, lineType=cv.LINE_AA)
            y_orig += text_height + 10

        return frame

    @staticmethod
    def __overlay_bot_right(frame, text_lines, color, frame_shape):
        y_height, x_width = frame_shape[0], frame_shape[1]
        y_orig = y_height - ((cv.getTextSize(text_lines[0], cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0][1] + 10)
                             * len(text_lines)) + 20

        for line in text_lines:
            text_width, text_height = cv.getTextSize(line, cv.FONT_HERSHEY_SIMPLEX, 1, 1)[0]
            x_orig = x_width - text_width - 10
            cv.putText(frame, line, (x_orig, y_orig), cv.FONT_HERSHEY_SIMPLEX, 1, color, 1, lineType=cv.LINE_AA)
            y_orig += text_height + 10

        return frame
