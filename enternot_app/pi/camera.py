import numpy as np


class Camera:
    def __init__(self):
        self.capture_frame()

    def capture_frame(self):
        self._frame = np.random.randint(256, size=(90*2, 160*2, 3), dtype=np.uint8)

    def get_current_frame(self):
        return self._frame
