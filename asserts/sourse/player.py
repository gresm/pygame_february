from typing import Union, Sequence, List, AnyStr, Tuple, Optional

import pygame as p

import settings
import base_app
from vector2 import Vector2
import asserts.graphics.graphics_manager as graphics
import asserts.maps.maps_manager as maps


class Player(p.sprite.Sprite):
    def __init__(self, x: int, y: int, player_sprite: graphics.MultipleStateAnimatedSprite, level: "Level",
                 hit_box: Optional[p.Rect] = None):
        super().__init__()
        self.sprite = player_sprite
        self.spawn_x = x
        self.spawn_y = y
        self.x = x
        self.y = y
        self.hit_box = hit_box.copy() if hit_box else player_sprite.image.get_rect()
        self.level = level
        self.cache: List[Tuple[int, int]] = [(self.x, self.y)]
        self.x_vel = 0
        self.y_vel = 0
        self.on_ground = False
        self.touch_wall = False
        self.gravity = settings.GRAVITY
        self.jump_power = settings.PLAYER_JUMP_POWER
        self.speed = settings.PLAYER_SPEED
        self.global_friction = settings.PLAYER_NORMAL_FRICTION
        self.ground_friction = settings.PLAYER_ON_GROUND_FRICTION

    @property
    def pos(self):
        return Vector2(self.x, self.y)

    @property
    def image(self):
        return self.sprite

    @property
    def rect(self):
        return self.sprite.rect

    def apply_friction(self):
        if self.touch_wall:
            self.x_vel *= self.ground_friction
            self.y_vel *= self.ground_friction
        else:
            self.x_vel *= self.global_friction
            self.y_vel *= self.global_friction

    def get_debug(self) -> Tuple[bool, bool, bool, bool, bool]:
        center = self.collide_with_walls()
        self.hit_box.x -= settings.PLAYER_MOVE_CHECK_RANGE
        left = self.collide_with_walls()
        self.hit_box.x += settings.PLAYER_MOVE_CHECK_RANGE * 2
        right = self.collide_with_walls()
        self.hit_box.x -= settings.PLAYER_MOVE_CHECK_RANGE
        self.hit_box.y += settings.PLAYER_MOVE_CHECK_RANGE
        top = self.collide_with_walls()
        self.hit_box.y -= settings.PLAYER_MOVE_CHECK_RANGE * 2
        down = self.collide_with_walls()
        self.hit_box.y += settings.PLAYER_MOVE_CHECK_RANGE

        return center, left, right, top, down

    def update(self):
        center, left, right, top, down = self.get_debug()
        self.on_ground = down
        self.touch_wall = any([left, right, top, down])

    def collide_with_walls(self):
        return bool(self.hit_box.collidelistall(self.level.get_walls_hit_box()))

    def apply_velocity(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def save_to_cache(self):
        self.cache.append((self.x, self.y))

    def is_dead(self) -> bool:
        return bool(self.hit_box.collidelist(self.level.get_spikes_hit_box()))


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
        self.win_cords = le[1]
        self.map = le[2]
        self.map_sprites_group = GlobalizedSprites()
        self.win_sprite = graphics.get_sprite("win", settings.MAX_ANIMATION_TICKS, self.win_cords[0] * 32,
                                              self.win_cords[1] * 32)
        self.win_group = p.sprite.Group()
        self.walls = p.sprite.Group()
        self.spikes = p.sprite.Group()
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                self.add_tile(graphics.get_sprite(graphics.SPRITES[self.map[x][y]],
                                                  settings.MAX_ANIMATION_TICKS, x * 32, y * 32),
                              graphics.SPRITES[self.map[x][y]])

    def add_tile(self, tile: graphics.AnimatedSprite, tile_name):
        self.map_sprites_group.add(tile)
        if tile_name in graphics.SPIKES:
            self.spikes.add(tile)
        if tile_name in graphics.WALLS:
            self.walls.add(tile)
        if tile_name == graphics.WIN:
            self.win_group.add(tile)

    def get_walls_hit_box(self):
        ret = []
        e: Union[graphics.MultipleStateAnimatedSprite, graphics.AnimatedSprite]
        for e in self.walls.sprites():
            ret.append(e.hit_box)
        return ret

    def get_spikes_hit_box(self):
        ret = []
        e: Union[graphics.MultipleStateAnimatedSprite, graphics.AnimatedSprite]
        for e in self.spikes.sprites():
            ret.append(e.hit_box)
        return ret

    def get_wins_hit_box(self):
        ret = []
        e: Union[graphics.MultipleStateAnimatedSprite, graphics.AnimatedSprite]
        for e in self.spikes.sprites():
            ret.append(e.hit_box)
        return ret


class App(base_app.BaseApp):
    def __init__(self, title="load again", icon_path: AnyStr = "../graphic/icon.png", height: int = 300,
                 width: int = 300, bg_color: Tuple[int, int, int] = (0, 0, 0), create_new_screen: bool = True):
        super().__init__(title, icon_path, height, width, bg_color, create_new_screen)
        self.level = Level(1)
        self.player = Player(self.level.spawn[0], self.level.spawn[1],
                             graphics.get_player_sprite(settings.PLAYER_ANIMATION_TICKS, *self.spawn), self.level,
                             p.Rect(*self.spawn, *settings.PLAYER_SIZE))

    @property
    def spawn(self):
        return self.level.spawn[0], self.level.spawn[1]

    def on_key_pressed(self, key_code: int):
        if key_code == p.K_ESCAPE:
            self.on_exit()

    def on_key_down(self, key_code: int):
        pass

    def on_key_up(self, key_code: int):
        pass

    def game_loop(self):
        pass
