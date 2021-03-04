import pygame as p

import asserts.sourse.player as player
import asserts.sourse.settings as settings


# noinspection PyUnusedLocal
def main(v=False):
    p.init()
    print(v)
    app = player.App(height=settings.HEIGHT, width=settings.WIDTH, bg_color=settings.BG_COLOR)
    app.run()
    p.exit()


if __name__ == '__main__':
    main()
    exit()
