from typing import List, Tuple, Union, Optional, Dict
from enum import Enum
import pygame as p

SPRITES = (
    "spikes_floor", "spikes_left", "spikes_right", "spikes_ceiling", "spikes_floating", "wall_bottom",
    "wall_bottom_left", "wall_bottom_right", "wall_center", "wall_flat_top", "wall_flat_top_left_corner",
    "wall_flat_top_right_corner", "wall_floating", "wall_floating_both", "wall_floating_left",
    "wall_floating_right", "wall_left_n_right", "wall_open_left", "wall_open_right", "wall_top"
)

SPIKES = (
    "spikes_floor", "spikes_left", "spikes_right", "spikes_ceiling", "spikes_floating"
)

WALLS = (
    "wall_bottom", "wall_bottom_left", "wall_bottom_right", "wall_center", "wall_flat_top",
    "wall_flat_top_left_corner", "wall_flat_top_right_corner", "wall_floating", "wall_floating_both",
    "wall_floating_left", "wall_floating_right", "wall_left_n_right", "wall_open_left", "wall_open_right", "wall_top"
)

SPRITE_HIT_BOXES: Dict[str, Tuple[int, int, int, int]] = {
    "spikes_floor": (0, 16, 32, 16),
    "spikes_left": (0, 0, 16, 32),
    "spikes_right": (16, 0, 16, 32),
    "spikes_ceiling": (0, 0, 32, 16)
}


class AnimatedSprite(p.sprite.Sprite):
    def __init__(self, frames: Union[List[p.Surface], Tuple[p.Surface]], max_ticks: int, x: int = 0, y: int = 0,
                 hit_box: Optional[p.Rect] = None, *groups: p.sprite.AbstractGroup):
        super().__init__(*groups)
        self._real_x = x
        self._real_y = y
        self.offset_x = 0
        self.offset_y = 0
        self.frames = [s.convert_alpha() for s in frames]
        self.frame = 0
        self.update_image()
        self.rect = self.image.get_rect()
        self.hit_box_default = hit_box if hit_box else self.image.get_rect().copy()
        self.max_ticks = max_ticks
        self.tick_count = 0

    @property
    def x(self):
        return self._real_x + self.offset_x

    @x.setter
    def x(self, value: int):
        self._real_x = value

    @property
    def y(self):
        return self._real_y + self.offset_x

    @y.setter
    def y(self, value: int):
        self._real_x = value

    @property
    def hit_box(self) -> p.Rect:
        h = self.hit_box_default.copy()
        h.x += self.x
        h.y += self.x
        return h

    def set_offset(self, x: int, y: int):
        self.offset_x = x
        self.offset_y = y

    def move_offset(self, x: int, y: int):
        self.offset_x += x
        self.offset_y += y

    def collide_with(self, other:  Union["AnimatedSprite", "MultipleStateAnimatedSprite"]):
        return self.rect.colliderect(other.hit_box)

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


def get_sprite(name: str, ticks: int, x: int = 0, y: int = 0, hit_box: Optional[Tuple[int, int, int, int]] = None) \
        -> AnimatedSprite:
    h = hit_box
    if not hit_box and name in SPRITE_HIT_BOXES:
        h = SPRITE_HIT_BOXES[name]

    # noinspection PyProtectedMember
    s = Sprites._get_sprite(name, ticks, x, y, h)
    return s


class Sprites(Enum):
    def __getattribute__(self, item: str) -> "AnimatedSprite":
        if len(item) >= 1 and item[0] == "_":
            return object.__getattribute__(self, item)
        return object.__getattribute__(self, "_get_sprite")(item)

    @staticmethod
    def _get_sprite(item: str, max_ticks: int, x: int, y: int, hit_box: Optional[Tuple[int, int, int, int]] = None) \
            -> "AnimatedSprite":
        if item in SPRITES:
            f = item + ".png"
            s = item + "_2.png"
            fd = item + "_3.png"
            ft = item + "_4.png"
            return AnimatedSprite([p.image.load(f), p.image.load(s), p.image.load(fd), p.image.load(ft)], max_ticks, x,
                                  y, hit_box)
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


class MultipleStateAnimatedSprite(p.sprite.Sprite):
    def __init__(self, states: Dict[str, AnimatedSprite], current_state: str):
        super().__init__()
        self.states = states
        self.state = self.states[current_state]

    @property
    def image(self):
        return self.state.image

    @property
    def rect(self):
        return self.state.rect

    @property
    def x(self):
        return self.state.x

    @x.setter
    def x(self, value: int):
        self.state.x = value

    @property
    def y(self):
        return self.state.y

    @y.setter
    def y(self, value: int):
        self.state.y = value

    @property
    def hit_box(self):
        return self.state.hit_box

    @property
    def hit_box_default(self):
        return self.state.hit_box_default

    def set_state(self, state: str):
        self.state = self.states[state]

    def move(self, x: int, y: int):
        self.state.move(x, y)

    def goto(self, x: int, y: int):
        self.state.goto(x, y)

    def update(self, *args, **kwargs) -> None:
        self.state.update()

    def collide_with(self, other:  Union["AnimatedSprite", "MultipleStateAnimatedSprite"]):
        return self.rect.colliderect(other.hit_box)

    def set_offset(self, x: int, y: int):
        self.state.set_offset(x, y)

    def move_offset(self, x: int, y: int):
        self.state.move_offset(x, y)
