import time
from threading import Thread, Condition
import cv2

try:
    import Adafruit_PCA9685
except ImportError:
    motorlib = None

try:
    # todo, replace pycamera with real library name
    from picamera import PiCamera
except ImportError:
    pycamera = None

import numpy as np

FRAME_SIZE = (768, 1024)
FRAME_RATE = 4  # 4 FPS = 1 frame every 250 ms
IMG_PATH = 'image.jpg'
LEFTRIGHT_MOTOR = 0
UPDOWN_MOTOR = 3




class Camera:
    def __init__(self, firebase=None):
        #init camera
        self._camera = PiCamera()
        self._camera.resolution = (1024, 768)
        self._camera.start_preview()
        self._detect_motion = True

        #init camera motor
        if motorlib is None:
            print("lib for motor is missing")
        else:
            self._pwm = Adafruit_PCA9685.PCA9685()


        # initialize frame to a black image
        self._frame = np.zeros(FRAME_SIZE + (3,), np.uint8)
        self._firebase = firebase

        self._condition = Condition()
        self._thread = Thread(target=self._capture_loop,
                              name="Camera-Capture-Thread",
                              daemon=True)  # kill this thread when Flask thread exits
        self._thread.start()

    @property
    def frame(self):
        return self._frame

    def wait_for_next_frame(self):
        with self._condition:
            self._condition.wait()

    def _capture_loop(self):
        while True:
            start_time = time.time()
            with self._condition:
                movement = self._capture_frame()
                if movement and self._firebase is not None:
                    self._firebase.send_movement_push_notification()
                self._condition.notify_all()

            delta = time.time() - start_time
            to_sleep = (1 / FRAME_RATE) - delta
            if to_sleep > 0:
                time.sleep(to_sleep)

    def _capture_frame(self):
        # if not running on the raspi:
        if pycamera is None:
            self._frame = np.random.randint(256, size=FRAME_SIZE + (3,), dtype=np.uint8)
        else:   # running on the raspi:
            # capture it
            self._camera.capture(IMG_PATH)
            self._frame = cv2.read(IMG_PATH)
        movement_detected = False  # TODO
        return movement_detected

    def move(self, degrees, direction):
        self._detect_motion = False
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
            timeout = 0.035
            degrees = degrees * -1

        while degrees >= 0:
            self._pwm.set_pwm(motor_index, 0, pulse_value)
            time.sleep(timeout)
            self._pwm.set_pwm(motor_index, 0, 0)
            degrees = degrees - 15
            time.sleep(0.5)

        self._detect_motion = True
