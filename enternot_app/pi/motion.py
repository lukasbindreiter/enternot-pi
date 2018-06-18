import numpy as np


class MotionDetector:
    def __init__(self):
        self.motion = []
        self.last_frame = None

    def analyze_frame(self, frame):
        """
        Analyze the given frame and detect motion compared to the last frame

        Args:
            frame: The new frame to analyze
        """
        if self.last_frame is not None:
            motion = self._detect_motion(self._last_frame, frame)
            self.motion.append(motion)
            # if the motion array gets too large, keep only the last
            # few entries
            if len(self.motion) > 200:
                self.motion = self.motion[-20:]

        self.last_frame = frame

    def motion_detected(self, n_frames=10):
        """
        Check if there was motion detected in all of the last n frames.

        Args:
            n_frames: Number of frames in which motion has to be detected
                consecutively.

        Returns:
            True if in all of the last n frames motion was detected, false
            otherwise
        """
        if len(self.motion) < n_frames:
            return False

        return all(self.motion[-n_frames:])

    def _detect_motion(self, prev_frame, curr_frame):
        if prev_frame is None or curr_frame is None:
            return False

        # convert from uint8 to int in order to avoid overflow
        # for negative differences
        prev_frame = prev_frame.astype(np.int)
        curr_frame = curr_frame.astype(np.int)

        # calculate difference for each axis
        diff = np.sqrt((curr_frame - prev_frame) ** 2)
        # sum up the diff for all three axes
        diff = np.sum(diff, axis=2)

        # if pixel difference value > 60, classify the pixel
        # as containing movement
        movement_mask = diff > 100

        # if more than 10 percent of the image has changed -> movement detected
        percentage = movement_mask.sum() / movement_mask.size
        return percentage > 0.1
