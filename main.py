import pygame as p

import asserts.sourse.player as player
import asserts.sourse.settings as settings


# noinspection PyUnusedLocal
def main():
    p.init()
    app = player.App(height=settings.HEIGHT, width=settings.WIDTH, bg_color=settings.BG_COLOR)
    app.run()
    p.quit()


if __name__ == '__main__':
    main()
    exit()
