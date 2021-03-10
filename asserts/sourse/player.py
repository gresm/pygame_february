from typing import Union, Sequence, List, AnyStr, Tuple, Optional

import pygame as p

import asserts.graphics.graphics_manager as graphics
import asserts.maps.maps_manager as maps
import asserts.sourse.base_app as base_app
import asserts.sourse.settings as settings
from asserts.sourse.vector2 import Vector2


class Player(p.sprite.Sprite):
    def __init__(self, x: int, y: int, player_sprite: graphics.MultipleStateAnimatedSprite, level: "Level", app: "App",
                 hit_box: Optional[p.Rect] = None):
        super().__init__()
        self.screen = app.screen
        self.sprite = player_sprite
        self.spawn = Vector2(x, y)
        self.__pos = Vector2(x, y)
        self.time = 0
        self.hit_box = hit_box.copy() if hit_box else player_sprite.image.get_rect()
        self.level = level
        self.cache: List[Tuple[int, int, ]] = [(self.pos.x, self.pos.y)]
        self.vel = Vector2(0, 0)
        self.on_ground = False
        self.touch_wall = False
        self.gravity = settings.GRAVITY
        self.jump_power = settings.PLAYER_JUMP_POWER
        self.speed = settings.PLAYER_SPEED
        self.global_friction = settings.PLAYER_NORMAL_FRICTION
        self.ground_friction = settings.PLAYER_ON_GROUND_FRICTION
        self.__jumping = False

    @property
    def pos(self):
        return self.__pos

    @property
    def image(self):
        return self.sprite

    @property
    def rect(self):
        return self.sprite.rect

    @property
    def jumping(self):
        return self.__jumping

    def apply_friction(self):
        if self.touch_wall:
            self.__pos *= self.ground_friction
        else:
            self.vel *= self.global_friction

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
        self.__pos += self.vel

    def save_to_cache(self):
        self.cache.append((self.pos.x, self.pos.y))

    @property
    def is_dead(self) -> bool:
        return bool(self.hit_box.collidelist(self.level.get_spikes_hit_box()))

    def dead(self):
        return KilledPlayer(self)

    def loop(self):
        self.time += 1
        self.save_to_cache()
        self.apply_velocity()
        self.update()
        if self.is_dead:
            self.level.add_dead_player(self.dead())

    def jump(self):
        self.__jumping = True
        while self.__jumping:
            self.pos.y += self.vel.y
            self.vel.y -= self.gravity
            self.__jumping = self.vel.y >= -10
            yield
        return

    def right(self):
        pass

    def left(self):
        pass

    def draw(self):
        self.sprite.move(*self.pos.serialize())
        self.screen.blit(self.sprite, area=self.rect)


class KilledPlayer:

    def __init__(self, player: Player):
        self.time = 0
        self.cache = player.cache
        self.__spawn = player.spawn
        self.__pos = self.__spawn
        self.__end_pos = player.pos
        self.__go = True

    @property
    def spawn(self):
        return self.__spawn

    @property
    def pos(self):
        return self.__pos

    def load_from_cache(self):
        if self.__go:
            if self.pos == self.__end_pos:
                self.__go = False
            else:
                self.__pos = self.cache[self.time]

    def loop(self):
        self.time += 1
        self.load_from_cache()


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
    def __init__(self, win=False):
        self.win = win
        msgs = ["Game Over"]
        if win:
            msgs.append("You win!")
        else:
            msgs.append("You lose")
        super(EndGame, self).__init__("\n".join(msgs))


class Level:
    def __init__(self, level: int):
        le = maps.load_level(level)
        if not le:
            raise EndGame(True)
        self.spawn = Vector2.deserialize(le[0])
        self.win_cords = Vector2.deserialize(le[1])
        self.map = le[2]
        self.map_sprites_group = GlobalizedSprites()
        self.win_sprite = graphics.get_sprite("win", settings.MAX_ANIMATION_TICKS, self.win_cords.x * 32,
                                              self.win_cords.y * 32)
        self.win_group = p.sprite.Group()
        self.walls = p.sprite.Group()
        self.spikes = p.sprite.Group()
        for x in range(len(self.map)):
            for y in range(len(self.map[x])):
                self.add_tile(graphics.get_sprite(graphics.SPRITES[self.map[x][y]],
                                                  settings.MAX_ANIMATION_TICKS, x * 32, y * 32),
                              graphics.SPRITES[self.map[x][y]])
        self.memories = []

    def add_tile(self, tile: graphics.AnimatedSprite, tile_name):
        self.map_sprites_group.add(tile)
        if tile_name in graphics.SPIKES:
            self.spikes.add(tile)
        if tile_name in graphics.WALLS:
            self.walls.add(tile)
        if tile_name == graphics.WIN:
            self.win_group.add(tile)

    def add_dead_player(self, cache):
        self.memories.append(cache)

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

    def loop(self):
        for dead_player in self.memories:
            dead_player.loop()


class App(base_app.BaseApp):
    def __init__(self, title="load again", icon_path: AnyStr = "../graphics/icon.png", height: int = 300,
                 width: int = 300, bg_color: Tuple[int, int, int] = (0, 0, 0), create_new_screen: bool = True):
        super().__init__(title, icon_path, height, width, bg_color, create_new_screen)
        self.level = Level(1)
        self.player = Player(self.level.spawn.x, self.level.spawn.y,
                             graphics.get_player_sprite(settings.PLAYER_ANIMATION_TICKS, *self.spawn), self.level,
                             p.Rect(*self.spawn, *settings.PLAYER_SIZE))

    @property
    def spawn(self):
        return self.level.spawn.x, self.level.spawn.y

    # TODO: in version 3.10 it is added match (like switch because in the python!) CleanCode
    def on_key_pressed(self, key_code: int):
        if key_code == p.K_ESCAPE:
            self.on_exit()
        if (key_code == p.K_SPACE) or (key_code == p.K_W) or (key_code == p.K_UP):
            self.player.jump()
        if (key_code == p.K_A) or (key_code == p.K_LEFT):
            pass
        if (key_code == p.K_D) or (key_code == p.K_RIGHT):
            pass

    def on_key_down(self, key_code: int):
        pass

    def on_key_up(self, key_code: int):
        pass

    def game_loop(self):
        self.player.loop()
        self.level.loop()

    def draw(self):
        self.player.draw()
