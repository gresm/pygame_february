from typing import Union, Sequence, List

import pygame as p

import base_app
from vector2 import Vector2
import asserts.graphics.graphics_manager as graphics


class Player:
    def __init__(self):
        x = 0
        y = 0
        self.pos = Vector2(x, y)


class GlobalizedSprites(p.sprite.Group):
    def __init__(self, *sprites: Union[Union[graphics.AnimatedSprite, graphics.MultipleStateAnimatedSprite],
                                       Sequence[Union[graphics.AnimatedSprite, graphics.MultipleStateAnimatedSprite]]]):
        super().__init__(*sprites)
        self.global_x = 0
        self.global_y = 0

    def add(self, *sprites: Union[graphics.AnimatedSprite, graphics.MultipleStateAnimatedSprite]) -> None:
        return super().add(*sprites)

    def update(self, *args, **kwargs) -> None:
        # noinspection PyTypeChecker
        e: List[Union[graphics.AnimatedSprite, graphics.MultipleStateAnimatedSprite]] = self.sprites()
        for v in e:
            v.set_offset(self.global_x, self.global_y)
        super().update(*args, **kwargs)

    def get_hit_boxes(self):
        # noinspection PyTypeChecker
        e: List[Union[graphics.AnimatedSprite, graphics.MultipleStateAnimatedSprite]] = self.sprites()
        ret: List[p.Rect] = []
        for v in e:
            ret.append(v.hit_box)


class App(base_app.BaseApp):
    def __init__(self, power):
        super().__init__()
        self.player = Player()
        self.v = 0
        self.h = 0
        self.power = power

    def on_key_pressed(self, key_code: int):
        if key_code == p.K_ESCAPE:
            self.on_exit()

    def on_key_down(self, key_code: int):
        pass

    def on_key_up(self, key_code: int):
        self.v = 3
        self.h = 1

    def _on_key_up(self):
        self.player.pos.y += self.v
        self.player.pos.y += self.h
        self.v -= 0.1 * self.power
        self.v -= 0.1 * self.power - 1
