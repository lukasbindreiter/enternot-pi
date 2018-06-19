import time
from threading import Thread, Condition

import cv2
import numpy as np

from enternot_app.pi.motion import MotionDetector

try:
    import Adafruit_PCA9685

    motorlib = True
except ImportError:
    motorlib = False

try:
    from picamera import PiCamera

    cameralib = True
except ImportError:
    cameralib = False

from enternot_app import Firebase

FRAME_SIZE = (384, 512)
FRAME_RATE = 2  # 2 FPS = 1 frame every 250 ms
IMG_PATH = 'frame.jpg'
LEFTRIGHT_MOTOR = 0
UPDOWN_MOTOR = 3
MIN_ANGLE = 36


class Camera:
    def __init__(self, firebase = None):
        self._firebase = firebase
        self._motion_dector = MotionDetector()
        # init camera
        if cameralib:
            self._camera = PiCamera()
            self._camera.resolution = (1024, 768)
            print("camera initialized")
        else:
            print("Pi camera not detected!")
            self._camera = None

        self._detect_motion = True

        # init camera motor
        # this needs to be available regardless if
        # motorlib is there or not, otherwise testing
        # is not possible without motorlib
        self._up_down_angle = 0
        self._left_right_angle = 0
        if motorlib:
            self._pwm = Adafruit_PCA9685.PCA9685()
            self._pwm.set_pwm_freq(60)
            print("Motor initialized")
        else:
            print("Lib for motor is missing")
            self._pwm = None

        # initialize frame to a black image
        self._frame = np.zeros(FRAME_SIZE + (3,), np.uint8)

        self._frame_lock = Condition()

        # set daemon to true to kill this thread when the main flask
        # thread exists
        self._capture_thread = Thread(target=self._capture_loop,
                                      name="Camera-Capture-Thread")
        self._capture_thread.daemon = True
        self._capture_thread.start()

        if self._pwm is not None:
            self._move_thread = Thread(target=self._move_loop,
                                       name="Camera-Move-Thread")
            self._move_thread.daemon = True
            self._move_thread.start()

    @property
    def frame(self):
        return self._frame

    def wait_for_next_frame(self):
        with self._frame_lock:
            self._frame_lock.wait()

    def _capture_loop(self):
        """
        Capture a frame 4 times a second. After each capture, check for
        movement
        """
        while True:
            start_time = time.time()
            with self._frame_lock:
                self._capture_frame()
                if self._detect_motion and self._motion_dector.motion_detected(
                        10):
                    if self._firebase is not None:
                        self._firebase.send_movement_push_notification()
                self._frame_lock.notify_all()

            delta = time.time() - start_time
            to_sleep = (1 / FRAME_RATE) - delta
            if to_sleep > 0:
                time.sleep(to_sleep)

    def _capture_frame(self):
        # if not running on the raspi:
        if self._camera is None:
            self._frame = np.zeros(shape=FRAME_SIZE + (3,), dtype=np.uint8)
            self._frame[:, :] = np.random.randint(256, size=(3,),
                                                  dtype=np.uint8)
        else:  # running on the raspi:
            # capture it
            self._camera.capture(IMG_PATH)
            self._frame = cv2.imread(IMG_PATH)

            if self._detect_motion:
                self._motion_dector.analyze_frame(self._frame)
            else:
                self._motion_dector.analyze_frame(None)

    def accumulate_angle(self, angle, direction):
        if direction == 1:
            self._left_right_angle += angle
        else:
            self._up_down_angle += angle

    def _move_loop(self):
        while True:
            if self._up_down_angle >= MIN_ANGLE:
                self._up_down_angle -= MIN_ANGLE
                self.move(MIN_ANGLE, 2)
            if self._up_down_angle <= MIN_ANGLE * -1:
                self._up_down_angle += MIN_ANGLE
                self.move(MIN_ANGLE * -1, 2)
            if self._left_right_angle >= MIN_ANGLE:
                self._left_right_angle -= MIN_ANGLE
                self.move(MIN_ANGLE, 1)
            if self._left_right_angle <= MIN_ANGLE * -1:
                self._left_right_angle += MIN_ANGLE
                self.move(MIN_ANGLE * -1, 2)
            time.sleep(0.5)

    def move(self, degrees, direction):
        if direction == 1:
            # move left/right
            motor_index = 0
        else:
            # move up/down
            motor_index = 3

        if degrees >= 0:
            pulse_value = 150
            timeout = 0.01
        else:
            pulse_value = 600
            if direction == 1:
                # timeout for left
                timeout = 0.04
            else:
                # timeout for up
                timeout = 0.029

        if self._pwm is not None:
            self._detect_motion = False
            self._pwm.set_pwm(motor_index, 0, pulse_value)
            time.sleep(timeout)
            self._pwm.set_pwm(motor_index, 0, 0)
            time.sleep(0.5)
            self._detect_motion = True
