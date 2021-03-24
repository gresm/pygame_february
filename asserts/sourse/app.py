from typing import Union, Sequence, List, AnyStr, Tuple, Optional

import pygame as p
from pygame.math import Vector2
from pygame.sprite import Sprite

import asserts.graphics.graphics_manager as graphics
import asserts.maps.maps_manager as maps
import asserts.sourse.base_app as base_app
import asserts.sourse.settings as settings
from asserts.graphics.graphics_manager import AnimatedSprite, MultipleStateAnimatedSprite


# noinspection PyUnusedLocal,PyUnreachableCode
def print_debug(*args):
    if __debug__:
        print(*args)


scale = Vector2(300, 300)


class Player(Sprite):
    def __init__(self, x: float, y: float, player_sprite: graphics.MultipleStateAnimatedSprite, app: "App",
                 hit_box: Optional[p.Rect] = None):
        super().__init__()
        self.sprite = player_sprite
        self.app = app
        self.__pos = Vector2(x, y)
        self.time = 0
        self.hit_box = hit_box.copy() if hit_box else player_sprite.image.get_rect()
        self.cache: List[Vector2] = [self.pos]
        self.vel = Vector2()
        self.on_ground = False
        self.touch_wall = False
        self.gravity = settings.GRAVITY
        self.jump_power = settings.PLAYER_JUMP_POWER
        self.speed = settings.PLAYER_SPEED
        self.global_friction = settings.PLAYER_NORMAL_FRICTION
        self.ground_friction = settings.PLAYER_ON_GROUND_FRICTION
        self.__jumping = False

    @property
    def level(self):
        return self.app.level

    @property
    def screen(self):
        return self.app.screen

    @property
    def spawn(self):
        return self.app.spawn

    @property
    def pos(self):
        return self.__pos

    @property
    def image(self):
        return self.sprite.image

    @property
    def rect(self):
        return self.sprite.rect

    @property
    def jumping(self):
        return self.__jumping

    def apply_friction(self):
        if self.touch_wall:
            self.__pos = self.pos * self.ground_friction
        else:
            self.vel = self.vel * self.global_friction

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

    def respawn(self):
        self.__pos = Vector2(self.spawn)

    def update(self):
        center, left, right, top, down = self.get_debug()
        self.on_ground = down
        self.touch_wall = any([left, right, top, down])
        self.sprite.update()
        self.sprite.goto(*self.pos)

    def collide_with_walls(self):
        return bool(self.hit_box.collidelistall(self.level.walls_hit_box))

    def save_to_cache(self):
        self.cache.append(self.pos)

    @property
    def is_dead(self) -> bool:
        return bool(self.hit_box.collidelist(self.level.spikes_hit_box))

    def dead(self):
        return KilledPlayer(self)

    def loop(self):
        print_debug(self.pos)
        self.time += 1
        self.save_to_cache()
        self.update()
        if self.is_dead:
            self.level.add_dead_player(self.dead())
            raise EndGame()
        if self.hit_box.collidelistall(self.level.wins_hit_box):
            raise EndGame(True)
        self.check_jump()

    def jump(self):
        self.vel.update(y=10)
        self.__jumping = True
        while self.__jumping:
            self.pos.update(y=self.pos.y + self.vel.y)
            self.vel.update(y=self.vel.y + self.gravity)
            self.__jumping = self.on_ground
            yield

    def check_jump(self):
        if self.jumping:
            self.jump()

    def right(self):
        self.pos.update(self.pos.x, self.pos.y + 10)

    def left(self):
        self.pos.update(self.pos.x, self.pos.y - 10)

    def draw(self):
        self.screen.blit(self.image, (self.pos[1], self.pos[0]))
        # self.screen.blit(self.image, (self.pos[1]+scale.x, self.pos[0]+scale.y))


class KilledPlayer:

    def __init__(self, player: Player):
        self.time = 0
        self.cache = player.cache
        self.__spawn = player.spawn
        self.__pos = player.pos
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

    def respawn(self):
        self.__pos = self.__spawn

    def draw(self):
        pass


class GlobalizedSprites(p.sprite.Group):
    def __init__(self, *sprites: Union[Sprite, Sequence[Sprite]]):
        super().__init__(*sprites)
        self.global_pos = Vector2()

    def update(self, *args, **kwargs) -> None:
        # noinspection PyTypeChecker
        e: List[Union[graphics.AnimatedSprite, graphics.MultipleStateAnimatedSprite]] = self.sprites()
        for v in e:
            v.set_offset(*self.global_pos.xy)
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
    levels = range(3)

    def __init__(self, level: int, app: "App"):
        self.app = app
        if level not in self.levels:
            raise EndGame(True)
        le = maps.load_level(level)
        self.spawn = le[0]
        self.win_cords = le[1]
        self.map: List[List[Union[int, float]]] = le[2]
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
                              graphics.SPRITES[self.map[x][y]], Vector2(x, y))
        self.memories = []
        self.level = level

    # noinspection PyUnusedLocal,GrazieInspection
    def add_tile(self, tile: AnimatedSprite, tile_name, pos: Vector2):
        self.map_sprites_group.add(tile)
        if tile_name in graphics.SPIKES:
            self.spikes.add(tile)
        if tile_name in graphics.WALLS:
            self.walls.add(tile)
        if tile_name == graphics.WIN:
            self.win_group.add(tile)

    def add_dead_player(self, cache):
        self.memories.append(cache)

    @property
    def walls_hit_box(self):
        ret = []
        e: Union[MultipleStateAnimatedSprite, AnimatedSprite]
        for e in self.walls.sprites():
            ret.append(e.hit_box)
        return ret

    @property
    def spikes_hit_box(self):
        ret = []
        e: Union[MultipleStateAnimatedSprite, AnimatedSprite]
        for e in self.spikes.sprites():
            ret.append(e.hit_box)
        return ret

    @property
    def wins_hit_box(self):
        ret = []
        e: Union[MultipleStateAnimatedSprite, AnimatedSprite]
        for e in self.spikes.sprites():
            if Vector2(e.x, e.y) == self.win_cords:
                ret.append(e.hit_box)
        return ret

    @property
    def screen(self):
        return self.app.screen

    def draw(self):
        for dead_player in self.memories:
            dead_player.draw()
        sprite: Union[graphics.AnimatedSprite, graphics.MultipleStateAnimatedSprite]
        for sprite in self.map_sprites_group.sprites():
            self.screen.blit(sprite.image, (sprite.y+scale.x, sprite.x+scale.y))

    def next_level(self):
        self.app.level = Level(self.level + 1, self.app)

    def respawn(self):
        for dead_player in self.memories:
            dead_player.respawn()

    def loop(self):
        for dead_player in self.memories:
            dead_player.loop()


class App(base_app.BaseApp):
    def __init__(self, title="load again", icon_path: AnyStr = "../graphics/icon.png", height: int = 300,
                 width: int = 300, bg_color: Tuple[int, int, int] = (0, 0, 0), create_new_screen: bool = True):
        super().__init__(title, icon_path, height, width, bg_color, create_new_screen)
        self.level = Level(1, self)
        self.player = Player(self.level.spawn.x, self.level.spawn.y,
                             graphics.get_player_sprite(settings.PLAYER_ANIMATION_TICKS, *self.spawn), self,
                             p.Rect(*self.spawn, *settings.PLAYER_SIZE))

    @property
    def spawn(self):
        return self.level.spawn.x, self.level.spawn.y

    # TODO: in version 3.10 it is added match (like switch because in the python!) #CleanCode
    def on_key_pressed(self, key_code: int):
        # match key_code:
        #     case p.K_ESCAPE:
        #         self.on_exit()
        #     case (key_code == p.K_SPACE) or (key_code == p.K_W) or (key_code == p.K_UP):
        #         self.player.jump()
        #     case (key_code == p.K_A) or (key_code == p.K_LEFT):
        #         self.player.left()
        #     case (key_code == p.K_D) or (key_code == p.K_RIGHT):
        #         self.player.right()
        if key_code == p.K_ESCAPE:
            self.on_exit()
        if (key_code == p.K_SPACE) or (key_code == p.K_w) or (key_code == p.K_UP):
            self.player.jump()
        if (key_code == p.K_a) or (key_code == p.K_LEFT):
            self.player.left()
        if (key_code == p.K_d) or (key_code == p.K_RIGHT):
            self.player.right()

    def on_key_down(self, key_code: int):
        pass

    def on_key_up(self, key_code: int):
        pass

    def game_loop(self):
        try:
            self.player.loop()
            self.level.loop()
        except EndGame as e:
            if e.win:
                self.level.next_level()
            self.player.respawn()
            self.level.respawn()

    def draw(self):
        self.player.draw()
        self.level.draw()
