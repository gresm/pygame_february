from copy import deepcopy
from unittest import TestCase

from app import *
from test_base_app import TestBaseApp


class TestPlayer(TestCase):

    def __init__(self, x: float, y: float, player_sprite: graphics.MultipleStateAnimatedSprite, app: "App",
                 hit_box: Optional[p.Rect] = None, methodName: str = 'runTest'):
        super(TestPlayer, self).__init__(methodName=methodName)
        self.player = Player(x, y, player_sprite, app, hit_box)

    def test_apply_friction(self):
        player_t = deepcopy(self.player)
        player_t.apply_friction()
        if self.player.touch_wall:
            self.failIf(player_t != player_t.pos * player_t.ground_friction)
        else:
            self.failIf(player_t.vel == player_t.vel * player_t.global_friction)

    def test_get_debug(self):
        player_t = deepcopy(self.player)
        center = player_t.collide_with_walls()
        player_t.hit_box.x -= settings.PLAYER_MOVE_CHECK_RANGE
        left = player_t.collide_with_walls()
        player_t.hit_box.x += settings.PLAYER_MOVE_CHECK_RANGE * 2
        right = player_t.collide_with_walls()
        player_t.hit_box.x -= settings.PLAYER_MOVE_CHECK_RANGE
        player_t.hit_box.y += settings.PLAYER_MOVE_CHECK_RANGE
        top = player_t.collide_with_walls()
        player_t.hit_box.y -= settings.PLAYER_MOVE_CHECK_RANGE * 2
        down = player_t.collide_with_walls()
        player_t.hit_box.y += settings.PLAYER_MOVE_CHECK_RANGE

        self.failIf([center, left, right, top, down] == player_t.get_debug())

    def test_update(self):
        pass

    def test_collide_with_walls(self):
        pass

    def test_save_to_cache(self):
        pass

    def test_is_dead(self):
        pass

    def test_loop(self):
        pass

    def test_jump(self):
        pass

    def test_right(self):
        pass

    def test_left(self):
        pass


class TestKilledPlayer(TestCase):

    def __init__(self, player: Player, methodName: str = "runTest"):
        super(TestKilledPlayer, self).__init__(methodName=methodName)
        self.killedPlayer = KilledPlayer(player)

    def test_load_from_cache(self):
        pass

    def test_loop(self):
        pass


class TestLevel(TestCase):

    def __init__(self, level: int, app: "App", methodName: str = "runTest"):
        super(TestLevel, self).__init__(methodName=methodName)
        self.level = Level(level, app)

    def test_add_tile(self):
        pass

    def test_walls_hit_box(self):
        pass

    def test_spikes_hit_box(self):
        pass

    def test_wins_hit_box(self):
        pass

    def test_loop(self):
        pass


class TestApp(TestBaseApp):

    def __init__(self, title="load again", icon_path: AnyStr = "../graphics/icon.png", height: int = 300,
                 width: int = 300, bg_color: Tuple[int, int, int] = (0, 0, 0), create_new_screen: bool = True,
                 methodName: str = 'runTest'):
        super(TestApp, self).__init__(methodName=methodName)
        self.app = App(title, icon_path, height, width, bg_color, create_new_screen)
        self.Level = TestLevel(self.app.level, self.app)
        self.Player = TestPlayer(self.app.level.spawn.x, self.app.level.spawn.y,
                                 graphics.get_player_sprite(settings.PLAYER_ANIMATION_TICKS, *self.app.spawn), self.app,
                                 p.Rect(*self.app.spawn, *settings.PLAYER_SIZE))

    def test_on_key_pressed(self):
        pass

    def test_on_key_down(self):
        pass

    def test_on_key_up(self):
        pass

    def test_game_loop(self):
        pass
