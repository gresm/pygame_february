from typing import Tuple, AnyStr as Path, Literal, Optional

import pygame

try:
    from asserts.graphics.graphics_manager import load_image
except ImportError:
    def load_image(name: str):
        return pygame.image.load(name)

all_keycodes = tuple(getattr(pygame.constants, key_str) for key_str in
                     filter(lambda k: k.startswith("K_"), dir(pygame.constants)))


class BaseApp:
    def __init__(self, title: Optional[str] = None, icon_path: Optional[Path] = None, height: int = 300,
                 width: int = 300, bg_color: Tuple[int, int, int] = (0, 0, 0), create_new_screen: bool = True):
        self.screen: pygame.Surface = pygame.display.set_mode((height, width)) \
            if create_new_screen else pygame.display.get_surface()
        if not self.screen:
            self.screen = pygame.display.set_mode((height, width))
        self.clock = pygame.time.Clock()
        self.delta = 0
        self.max_tps = 20
        self.running = True
        self.bg_color = bg_color
        self.event_info: Optional[pygame.event.Event] = None
        self.event_info_actual = False
        if icon_path:
            pygame.display.set_icon(load_image(icon_path))
        if title:
            pygame.display.set_caption(title)
        self.draw_background()

    @property
    def display(self):
        return pygame.display.get_surface()

    def run(self):
        """
        Function to run game\n
        Handles KeyboardInterrupt as exit command, but re-raises it after.
        """
        try:
            while self.running:
                # checking events
                self.check_events()

                # ticking
                self.delta += self.clock.tick() / 1000
                while self.delta > 1 / self.max_tps:
                    self.delta -= 1 / self.max_tps
                    # running loop
                    self.loop(self.delta)
        except KeyboardInterrupt as e:
            self.on_exit()
            raise KeyboardInterrupt from e

        self.on_exit()
        return

    def loop(self, delta: int):
        # checking events
        self.check_events()

        # game loop
        self.game_loop(delta)

        # drawing
        self.draw_background()
        self.draw()

        pygame.display.flip()

    def handle_input(self):
        keys_pressed = pygame.key.get_pressed()
        for keycode in all_keycodes:
            if keys_pressed[keycode]:
                self.on_key_pressed(keycode)
        return

    # noinspection PyMethodMayBeStatic
    def key_pressed(self, key_code: int) -> bool:
        return pygame.key.get_pressed()[key_code]

    def draw_background(self):
        self.screen.fill(self.bg_color)

    def on_exit(self):
        self.running = False

    def draw(self):
        """
        To override.
        :return:
        """
        pass

    def check_events(self):
        # handle pressed input
        self.handle_input()

        # handle mouse input
        self.handle_mouse_input()

        # checking events
        for event in pygame.event.get():
            self.handle_event(event)
        return

    def handle_mouse_input(self):
        keys = pygame.mouse.get_pressed(3)
        for i in range(len(keys)):
            if keys[i]:
                # noinspection PyTypeChecker
                self.on_mouse_pressed(pygame.mouse.get_pos(), i + 1)

    def handle_event(self, event: pygame.event.Event):
        self.event_info = event
        self.event_info_actual = True
        e = event.type
        if e == pygame.QUIT:
            self.on_exit()
        elif e == pygame.KEYDOWN:
            self.on_key_down(event.key)
        elif e == pygame.KEYUP:
            self.on_key_up(event.key)
        elif e == pygame.MOUSEBUTTONDOWN:
            self.on_mouse_button_down(pygame.mouse.get_pos(), event.button)
        elif e == pygame.MOUSEBUTTONUP:
            self.on_mouse_button_up(pygame.mouse.get_pos(), event.button)
        elif e == pygame.MOUSEMOTION:
            self.on_mouse_move(pygame.mouse.get_pos())
        else:
            self.on_event(event)
        self.event_info_actual = False

    def game_loop(self, delta: int):
        """
        To override.
        :return:
        """
        pass

    def on_key_pressed(self, key_code: int):
        """
        To override.
        :param key_code:
        :return:
        """
        pass

    def on_event(self, event: pygame.event.Event):
        """
        To override.
        :param event: event
        :return: None
        """
        pass

    def on_mouse_button_down(self, pos: Tuple[int, int], button_id: Literal[1, 2, 3, 4, 5]):
        """
        To override.
        :param button_id:
        :param pos:
        :return:
        """
        pass

    def on_mouse_button_up(self, pos: Tuple[int, int], button_id: Literal[1, 2, 3, 4, 5]):
        """
        To override.
        :param button_id:
        :param pos:
        :return:
        """
        pass

    def on_mouse_pressed(self, pos: Tuple[int, int], button_id: Literal[1, 2, 3, 4, 5]):
        """
        To override.
        :param button_id:
        :param pos:
        :return:
        """
        pass

    def on_mouse_move(self, pos: Tuple[int, int]):
        """
        To override.
        :param pos:
        :return:
        """
        pass

    def on_key_down(self, key_code: int):
        """
        To override.
        :param key_code: int
        :return: None
        """
        pass

    def on_key_up(self, key_code: int):
        """
        To override.
        :param key_code: int
        :return: None
        """
        pass
