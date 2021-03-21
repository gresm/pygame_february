from enum import Enum
from typing import Union

import pygame as p


class Sounds(Enum):
    bgm = "bgm.wav"


class SoundPlayer:
    def __init__(self, sound_path: Union[str, Sounds], loops: int = 0, sound_layer: int = -1, max_time: int = 0,
                 fade_ms: int = 0):
        self.sound_path = sound_path.value if isinstance(sound_path, Sounds) else sound_path
        self.sound_layer = self._get_fixed_sound_layer(sound_layer)
        self.loops = loops
        self.sound = p.mixer.Sound(self.sound_path)
        self.channel = p.mixer.Channel(self.sound_layer)
        self.max_time = max_time
        self.fade_ms = fade_ms

    def play(self):
        self.channel.play(self.sound, self.loops, self.max_time, self.fade_ms)

    def stop(self):
        self.channel.stop()

    def pause(self):
        self.channel.pause()

    def unpause(self):
        self.channel.unpause()

    def set_volume(self, *args, **kwargs):
        self.channel.set_volume(*args, **kwargs)

    def fadeout(self, time: int):
        self.channel.fadeout(time)

    def get_volume(self):
        return self.channel.get_volume()

    def get_busy(self):
        return self.channel.get_busy()

    @staticmethod
    def _get_fixed_sound_layer(layer: int) -> int:
        max_layers = p.mixer.get_num_channels()
        if layer < 0:
            new_l = max_layers + 2
            p.mixer.set_num_channels(new_l)
            return new_l - 1
        if layer > max_layers:
            p.mixer.set_num_channels(layer + 1)
            max_layers = p.mixer.get_num_channels()
            return max_layers
        return layer
