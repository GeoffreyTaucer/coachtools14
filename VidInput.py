import cv2 as cv
import numpy as np
import atexit


class Feed:
    def __init__(self, vid_src=0):
        self.cap = cv.VideoCapture(vid_src)
        self.motion_detector = MotionDetector(default=True)
        self.current_frame = None
        self.height = self.cap.get(cv.CAP_PROP_FRAME_HEIGHT)
        self.width = self.cap.get(cv.CAP_PROP_FRAME_WIDTH)
        self.fps = self.cap.get(cv.CAP_PROP_FPS)

        self.motion_frames = 0
        self.motionless_frames = 0
        self.motion_detected = False
        self.paused = False

        atexit.register(self.cap.release)

    def get_frame(self):
        _, frame = self.cap.read()
        self.check_movement(frame)
        return frame

    def check_movement(self, frame):
        is_moving = self.motion_detector.detect(frame)
        if is_moving:
            self.motion_frames += 1

            if self.motion_frames > 3:
                self.motionless_frames = 0

        else:
            self.motionless_frames += 1

            if self.motionless_frames > 3:
                self.motion_frames = 0

        self.motion_detected = self.motion_frames > 3


class MotionDetector:
    """
    Motion detector object.
    """

    def __init__(self, default=False, threshold=10, tolerance=200, kernel_size=7, erosions=3):
        self.default = default
        self.threshold = threshold
        self.tolerance = tolerance
        self.kernel = np.ones(kernel_size, np.uint8)
        self.erosion_iterations = erosions
        self.frames = []

        self.gray = None
        self.diff = None
        self.threshed = None
        self.denoised = None
        self.total_diff = 0
        self.is_moving = False

    def detect(self, frame):
        """
        Motion motion_detector

        Takes a frame, compares to previous frame received to check for change, performs some noise cleanup, then
        returns a boolean indicating whether the two frames are sufficiently different to be constitute movement.
        """
        self.gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        self.frames.insert(0, self.gray)

        if len(self.frames) < 2:
            return self.default

        while len(self.frames) > 2:
            del self.frames[-1]

        self.diff = cv.absdiff(self.frames[0], self.frames[1])
        _, self.threshed = cv.threshold(self.diff, self.threshold, 255, cv.THRESH_BINARY)
        self.denoised = cv.erode(self.threshed, self.kernel, iterations=self.erosion_iterations)
        self.total_diff = cv.countNonZero(self.denoised)

        self.is_moving = self.total_diff > self.tolerance

        return self.is_moving

    # def get_motion_composite(self, monitor): # doesn't work yet
    #     """
    #     Takes Take four frames and returns a composite frame
    #
    #     Takes monitor measurements (width, height) and four frames, and assembles those four frames to each take up
    #     one quadrant of the monitor
    #     """
    #     width = monitor.width
    #     height = monitor.height
    #     frames = (self.gray, self.diff, self.threshed, self.denoised)
    #     shrunk_frames = []
    #     for frame in frames:
    #         shrunk_frames.append(cv.resize(frame, (int(width / 2), int(height / 2)), interpolation=cv.INTER_AREA))
    #
    #     composite_frame = np.zeros((height, width), np.uint8)
    #     composite_frame[0:0, int(height / 2):int(width / 2)] = shrunk_frames[0]
    #     composite_frame[0:int(width / 2), int(height / 2):width] = shrunk_frames[1]
    #     composite_frame[int(height / 2):0, int(width / 2):height] = shrunk_frames[2]
    #     composite_frame[int(height / 2):int(width / 2), height:width] = shrunk_frames[3]
    #     # TODO add overlay to left side indicating threshold, tolerance, kernel_size, erosions
    #     # TODO add overlay to right side indicating total_diff/tolerance, is_moving
    #
    #     return composite_frame

    def reset_defaults(self):
        self.default = False
        self.threshold = 10
        self.tolerance = 200
        self.kernel = np.ones(7, np.uint8)
        self.erosion_iterations = 3
