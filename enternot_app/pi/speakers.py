import os
import pygame

# how long the sirene sound will be played by default (time in seconds)
SIRENE_PLAYBACK_DURATION = 3 * 60

# the sirene.wav file contains 8 seconds of audio
SIRENE_WAV_LENGTH = 8


class Speakers:
    def __init__(self):
        pygame.mixer.init()
        dir = os.path.dirname(__file__)
        self._sirene_filename = os.path.join(dir, "sirene.wav")

    def play_sirene(self):
        self.stop_playback()
        pygame.mixer.music.load(self._sirene_filename)
        loops = SIRENE_PLAYBACK_DURATION // SIRENE_WAV_LENGTH
        pygame.mixer.music.play(loops=loops)

    def stop_playback(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
