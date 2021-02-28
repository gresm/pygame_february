import pygame as p
import base_app
from vector2 import Vector2


class Player:

    def __init__(self):
        x = 0
        y = 0
        self.pos = Vector2(x, y)


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
        self.v -= 0.1 * self.power-1
