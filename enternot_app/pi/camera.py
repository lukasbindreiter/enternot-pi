import numpy as np
from threading import Thread, Condition
import time

FRAME_SIZE = (90 * 2, 160 * 2)
FRAME_RATE = 4  # 4 FPS = 1 frame every 250 ms


class Camera:
    def __init__(self):
        # initialize frame to a black image
        self._frame = np.zeros(FRAME_SIZE + (3,), np.uint8)
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
                self._capture_frame()
                self._condition.notify_all()

            delta = time.time() - start_time
            to_sleep = (1 / FRAME_RATE) - delta
            if to_sleep > 0:
                time.sleep(to_sleep)

    def _capture_frame(self):
        self._frame = np.random.randint(256, size=FRAME_SIZE + (3,), dtype=np.uint8)
