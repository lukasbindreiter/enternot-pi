import os
import pygame
import pydub

# how long the siren sound will be played by default (time in seconds)
SIREN_PLAYBACK_DURATION = 3 * 60

# the siren.wav file contains 8 seconds of audio
SIREN_WAV_LENGTH = 8


class Speakers:
    def __init__(self):
        try:
            pygame.mixer.init()
            self._audio_device = True
        except Exception as err:
            print("Failed to initialize speaker:")
            print(err)
            self._audio_device = False
        dir = os.path.dirname(__file__)
        self._siren_filename = os.path.join(dir, "siren.wav")
        self._recording_filename = os.path.join(dir, "recording.wav")

    def play_siren(self):
        if not self._audio_device:
            return 0
        self.stop_playback()
        pygame.mixer.music.load(self._siren_filename)
        loops = SIREN_PLAYBACK_DURATION // SIREN_WAV_LENGTH
        pygame.mixer.music.play(loops=loops)
        return SIREN_PLAYBACK_DURATION

    def play_byte_stream(self, data):
        if not self._audio_device:
            return 0

        self.stop_playback()

        sample_width = 2  # 16 bit pcm
        frame_rate = 16000  # sample rate
        channels = 2  # stereo signal

        audio = pydub.AudioSegment(data=data, sample_width=sample_width,
                                   frame_rate=frame_rate, channels=channels)

        audio.export(self._recording_filename, format="wav")
        pygame.mixer.music.load(self._recording_filename)
        pygame.mixer.music.play()

    def stop_playback(self):
        if not self._audio_device:
            return
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
