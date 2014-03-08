#!/usr/bin/env python
import sys
import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import HWSURFACE
from pygame.locals import QUIT

SCREENRECT = pygame.Rect(0, 0, 800, 600)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
       self.x = x
       self.y = y


def main():
    # Every Pygame program has the following:
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, DOUBLEBUF | HWSURFACE)

    # All games are essentially one giant loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit
                sys.exit()
        pygame.display.update()


if __name__ == "__main__":
    main()
