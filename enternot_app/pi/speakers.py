import os
import pygame

# how long the siren sound will be played by default (time in seconds)
SIREN_PLAYBACK_DURATION = 3 * 60

# the siren.wav file contains 8 seconds of audio
SIREN_WAV_LENGTH = 8


class Speakers:
    def __init__(self):
        try:
            pygame.mixer.init()
            self._audio_device = True
        except Exception:
            self._audio_device = False
        dir = os.path.dirname(__file__)
        self._siren_filename = os.path.join(dir, "siren.wav")

    def play_siren(self):
        if not self._audio_device:
            return 0
        self.stop_playback()
        pygame.mixer.music.load(self._siren_filename)
        loops = SIREN_PLAYBACK_DURATION // SIREN_WAV_LENGTH
        pygame.mixer.music.play(loops=loops)
        return SIREN_PLAYBACK_DURATION

    def stop_playback(self):
        if not self._audio_device:
            return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
