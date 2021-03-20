import os
from enum import Enum
from typing import List, Tuple, Union, Optional, Dict

import pygame as p

SPRITES = (
    "bg", "spikes_floor", "spikes_left", "spikes_right", "spikes_ceiling", "spikes_floating", "wall_bottom",
    "wall_bottom_left", "wall_bottom_right", "wall_center", "wall_flat_top", "wall_flat_top_left_corner",
    "wall_flat_top_right_corner", "wall_floating", "wall_floating_both", "wall_floating_left",
    "wall_floating_right", "wall_left_n_right", "wall_open_left", "wall_open_right", "wall_top", "win"
)
SPRITES_D = {
    0: "bg",
    1: "spikes_floor",
    2: "spikes_left",
    3: "spikes_right",
    4: "spikes_ceiling",
    5: "spikes_floating",
    6: "wall_bottom",
    7: "wall_bottom_left",
    8: "wall_bottom_right",
    9: "wall_center",
    10: "wall_flat_top",
    11: "wall_flat_top_left_corner",
    12: "wall_flat_top_right_corner",
    13: "wall_floating",
    14: "wall_floating_both",
    15: "wall_floating_left",
    16: "wall_floating_right",
    17: "wall_left_n_right",
    18: "wall_open_left",
    19: "wall_open_right",
    20: "wall_top",
    21: "win",
}

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

WIN = "win"


class AnimatedSprite(p.sprite.Sprite):
    def __init__(self, frames: Union[List[p.Surface], Tuple[p.Surface]], max_ticks: int, x: float = 0, y: float = 0,
                 hit_box: Optional[p.Rect] = None, steps: int = 1, *groups: p.sprite.AbstractGroup):
        super().__init__(*groups)
        self._real_x = x
        self._real_y = y
        self.offset_x = 0
        self.offset_y = 0
        self.frames = [s.convert_alpha() for s in frames]
        self.frame = 0
        self.steps = steps
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

    def set_offset(self, x: float, y: float):
        self.offset_x = x
        self.offset_y = y

    def move_offset(self, x: float, y: float):
        self.offset_x += x
        self.offset_y += y

    def collide_with(self, other: Union["AnimatedSprite", "MultipleStateAnimatedSprite"]):
        return self.rect.colliderect(other.hit_box)

    def update_image(self):
        self.image = self.frames[self.frame]

    def update_rect(self):
        self.rect = self.image.get_rect()
        self.update_cords()

    def update_cords(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def goto(self, x: float, y: float):
        self.x = x
        self.y = y

    def move(self, x: float, y: float):
        self.x += x
        self.y += y

    def tick(self) -> bool:
        self.tick_count += 1
        if self.tick_count % self.max_ticks == 0:
            self.next_frame()
            return True
        return False

    def next_frame(self):
        self.frame += self.steps
        self.frame %= len(self.frames)
        self.update_image()
        self.update_rect()

    def update(self, *args, **kwargs) -> None:
        self.tick()

    # noinspection PyMethodMayBeStatic
    def next_state(self) -> bool:
        return False


def load_image(name: str):
    return p.image.load(os.path.abspath("") + "/asserts/graphics/" + name)


def get_sprite(name: str, ticks: int, x: float = 0, y: float = 0, hit_box: Optional[Tuple[int, int, int, int]] = None,
               steps: int = 0) -> AnimatedSprite:
    f = name + ".png"
    s = name + "_2.png"
    fd = name + "_3.png"
    ft = name + "_4.png"
    return AnimatedSprite([load_image(f), load_image(s), load_image(fd), load_image(ft)], ticks, x,
                          y, hit_box, steps)


def get_chained_sprite(name: str, ticks: int, animation_loops, x: float = 0, y: float = 0,
                       hit_box: Optional[Tuple[int, int, int, int]] = None,
                       steps: int = 0) -> "ChainedAnimatedSprite":
    f = name + ".png"
    s = name + "_2.png"
    fd = name + "_3.png"
    ft = name + "_4.png"
    return ChainedAnimatedSprite([load_image(f), load_image(s), load_image(fd), load_image(ft)], ticks,
                                 animation_loops, x, y, hit_box, steps)


# noinspection PyUnusedLocal
def get_player_sprite(ticks: int, x: float, y: float) -> "MultipleStateAnimatedSprite":
    p_i = get_sprite("player_idle", ticks, x, y)
    p_f = get_sprite("player_fly", ticks, x, y)
    p_j_a = get_sprite("player_jump_abort", ticks, x, y)
    p_j_a_r = get_chained_sprite("player_jump_abort", ticks, x, y, steps=-1)
    p_c_s = get_sprite("player_ceiling_stick", ticks, x, y)
    p_s_j = get_sprite("player_start_jump", ticks, x, y)

    return MultipleStateAnimatedSprite({"idle": (p_i, "idle"), "fly": (p_f, "fly")}, "idle")


class Sprites(Enum):
    def __getattribute__(self, item: str) -> "AnimatedSprite":
        if len(item) >= 1 and item[0] == "_":
            return object.__getattribute__(self, item)
        return object.__getattribute__(self, "_get_sprite")(item)

    @staticmethod
    def _get_sprite(item: str, max_ticks: int, x: float, y: float, hit_box: Optional[Tuple[int, int, int, int]] = None) \
            -> "AnimatedSprite":
        if item in SPRITES:
            f = item + ".png"
            s = item + "_2.png"
            fd = item + "_3.png"
            ft = item + "_4.png"
            return AnimatedSprite([load_image(f), load_image(s), load_image(fd), load_image(ft)], max_ticks, x,
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
    win = ...


class ChainedAnimatedSprite(AnimatedSprite):
    def __init__(self, frames: Union[List[p.Surface], Tuple[p.Surface]], max_ticks: int,
                 max_animation_loops: int = 1, x: float = 0, y: float = 0, hit_box: Optional[p.Rect] = None,
                 steps: int = 1,
                 *groups: p.sprite.AbstractGroup):
        super().__init__(frames, max_ticks, x, y, hit_box, steps, *groups)
        self.max_animation_loops = max_animation_loops

    def next_state(self) -> bool:
        if self.max_animation_loops < 0:
            return False
        return self.tick_count / self.max_ticks >= self.max_animation_loops


class MultipleStateAnimatedSprite(p.sprite.Sprite):
    def __init__(self, states: Dict[str, Tuple[AnimatedSprite, str]], current_state: str):
        super().__init__()
        self.states = states
        self._state = self.states[current_state]

    @property
    def state(self):
        return self._state[0]

    @property
    def next_state_name(self):
        return self._state[1]

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

    @state.setter
    def state(self, state: str):
        self._state = self.states[state]

    def move(self, x: float, y: float):
        self.state.move(x, y)

    def goto(self, x: float, y: float):
        self.state.goto(x, y)

    def update(self, *args, **kwargs) -> None:
        self.tick()
        self.state.update()

    def tick(self) -> bool:
        if self.state.next_state():
            self.state = self.next_state_name
        return self.state.tick()

    def collide_with(self, other: Union["AnimatedSprite", "MultipleStateAnimatedSprite"]):
        return self.rect.colliderect(other.hit_box)

    def set_offset(self, x: float, y: float):
        self.state.set_offset(x, y)

    def move_offset(self, x: float, y: float):
        self.state.move_offset(x, y)
