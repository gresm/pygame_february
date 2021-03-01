from typing import Union, Sequence, List, AnyStr, Tuple


import pygame as p


import settings
import base_app
from vector2 import Vector2
import asserts.graphics.graphics_manager as graphics
import asserts.maps.maps_manager as maps


class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.pos = Vector2(x, y)


class GlobalizedSprites(p.sprite.Group):
    def __init__(self, *sprites: Union[p.sprite.Sprite, Sequence[p.sprite.Sprite]]):
        super().__init__(*sprites)
        self.global_x = 0
        self.global_y = 0

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


class EndGame(Exception):
    pass


class Level:
    def __init__(self, level: int):
        le = maps.load_level(level)
        if not le:
            raise EndGame
        self.spawn = le[0]
        self.map = le[1]
        self.map_sprites_group = GlobalizedSprites()
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                self.map_sprites_group.add(graphics.get_sprite(graphics.SPRITES[self.map[x][y]],
                                           settings.MAX_ANIMATION_TICKS, x*32, y*32))


class App(base_app.BaseApp):
    def __init__(self, title="load again", icon_path: AnyStr = "../graphic/icon.png", height: int = 300,
                 width: int = 300, bg_color: Tuple[int, int, int] = (0, 0, 0), create_new_screen: bool = True):
        super().__init__(title, icon_path, height, width, bg_color, create_new_screen)
        self.player = Player(0, 0)
        self.v = 0
        self.h = 0

    def on_key_pressed(self, key_code: int):
        if key_code == p.K_ESCAPE:
            self.on_exit()

    def on_key_down(self, key_code: int):
        pass

    def on_key_up(self, key_code: int):
        self.v = 3
        self.h = 1

    def game_loop(self):
        pass
