import pygame as p

import asserts.sourse.app as player
import asserts.sourse.settings as settings


def main():
    p.init()
    player.App(height=settings.HEIGHT, width=settings.WIDTH, bg_color=settings.BG_COLOR).run()
    p.quit()


if __name__ == '__main__':
    main()
    exit()
