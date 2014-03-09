#!/usr/bin/env python
import sys
import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import HWSURFACE
from pygame.locals import QUIT

SCREENRECT = pygame.Rect(0, 0, 800, 600)
FPS = 30
AQUA = (0, 255, 255)
LIGHT_GRAY = (200, 200, 200)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.bomb_size = 24
        self.half_bomb_size = self.bomb_size / 2
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((25, 25))
        pygame.draw.circle(
            self.image,
            LIGHT_GRAY,
            (self.half_bomb_size, self.half_bomb_size),
            self.half_bomb_size)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        print "update"
        pass


def main():
    # Every Pygame program has the following:
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, DOUBLEBUF | HWSURFACE)
    fpsClock = pygame.time.Clock()

    background = pygame.Surface((SCREENRECT.size))
    background.fill(AQUA)

    screen.blit(background, (0, 0))

    # Sprites
    all = pygame.sprite.OrderedUpdates()
    bomb = pygame.sprite.Group()
    Bomb.containers = all, bomb

    Bomb(40, 40)
    # All games are essentially one giant loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit
                sys.exit()

        all.clear(screen, background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
