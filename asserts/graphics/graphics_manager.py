from typing import List, Tuple, Union
from enum import Enum
import pygame as p


SPRITES = {
    "spikes_floor", "spikes_left", "spikes_right", "spikes_ceiling", "spikes_floating", "wall_bottom",
    "wall_bottom_left", "wall_bottom_right", "wall_center", "wall_flat_top", "wall_flat_top_left_corner",
    "wall_flat_top_right_corner", "wall_floating", "wall_floating_both", "wall_floating_left",
    "wall_floating_right", "wall_left_n_right", "wall_open_left", "wall_open_right", "wall_top"
}


class AnimatedSprite(p.sprite.Sprite):
    def __init__(self, frames: Union[List[p.Surface], Tuple[p.Surface]], max_ticks: int, x: int = 0, y: int = 0,
                 *groups: p.sprite.AbstractGroup):
        super().__init__(*groups)
        self.y = y
        self.x = x
        self.frames = [s.convert_alpha() for s in frames]
        self.frame = 0
        self.update_image()
        self.rect = self.image.get_rect()
        self.max_ticks = max_ticks
        self.tick_count = 0

    def update_image(self):
        self.image = self.frames[self.frame]

    def update_rect(self):
        self.rect = self.image.get_rect()
        self.update_cords()

    def update_cords(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def goto(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, x: int, y: int):
        self.x += x
        self.y += y

    def tick(self):
        self.tick_count += 1
        if self.tick_count % self.max_ticks == 0:
            self.next_frame()

    def next_frame(self):
        self.frame += 1
        if self.frame >= len(self.frames):
            self.frame = 0
        self.update_image()
        self.update_rect()

    def update(self, *args, **kwargs) -> None:
        self.tick()


def get_sprite(name: str, ticks: int, x: int = 0, y: int = 0) -> AnimatedSprite:
    # noinspection PyProtectedMember
    s = Sprites._get_sprite(name)
    s.max_ticks = ticks
    s.goto(x, y)
    return s


class Sprites(Enum):
    def __getattribute__(self, item: str) -> "AnimatedSprite":
        if len(item) >= 1 and item[0] == "_":
            return object.__getattribute__(self, item)
        return object.__getattribute__(self, "_get_sprite")(item)

    @staticmethod
    def _get_sprite(item: str) -> "AnimatedSprite":
        if item in SPRITES:
            f = item + ".png"
            s = item + "_2.png"
            fd = item + "_3.png"
            ft = item + "_4.png"
            return AnimatedSprite([p.image.load(f), p.image.load(s), p.image.load(fd), p.image.load(ft)], 1)
        else:
            raise AttributeError

    spikes_floor = ...
    spikes_left = ...
    spikes_right = ...
    spikes_ceiling = ...
    spikes_floating = ...
    wall_bottom = ...
    wall_bottom_left = ...
    wall_bottom_right = ...
    wall_center = ...
    wall_flat_top = ...
    wall_flat_top_left_corner = ...
    wall_flat_top_right_corner = ...
    wall_floating = ...
    wall_floating_both = ...
    wall_floating_left = ...
    wall_floating_right = ...
    wall_left_n_right = ...
    wall_open_left = ...
    wall_open_right = ...
    wall_top = ...
