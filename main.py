#!/usr/bin/env python
import sys
import pygame
from pygame.locals import DOUBLEBUF
from pygame.locals import HWSURFACE
from pygame.locals import QUIT
from pygame.locals import SRCALPHA
from pygame.locals import USEREVENT

SCREENRECT = pygame.Rect(0, 0, 800, 600)
FPS = 30
AQUA = (0, 255, 255)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (20, 20, 20)
DROP_BOMB = USEREVENT


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.bomb_size = 24
        self.half_bomb_size = self.bomb_size / 2
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((self.bomb_size, self.bomb_size), SRCALPHA)
        pygame.draw.circle(
            self.image,
            DARK_GRAY,
            (self.half_bomb_size, self.half_bomb_size),
            self.half_bomb_size)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

    def update(self):
        self.y += self.speed
        self.rect.center = (self.x, self.y)


class Bomber(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 400
        self.y = 30

        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((50, 200))
        self.image.fill(LIGHT_GRAY)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        # AKA the level
        self.madness = 1
        self.speed = 2 * self.madness
        self.bomb_rate_miliseconds = 2000
        self.num_bombs = 10

    def set_bomb_rate_miliseconds(self):
        brms = 2000 - (self.madness * 60)
        if brms <= 0:
            brms = 10
            return brms

    def update(self):
        self.rect.center = (self.x, self.y)
        pass

    def set_bomber_timer(self, rate):
        print self.bomb_rate_miliseconds
        pygame.time.set_timer(DROP_BOMB, rate)

    def drop_bomb(self):
        Bomb(self.x, self.y, self.speed)
        self.num_bombs = self.num_bombs - 1
        if self.num_bombs > 0:
            self.set_bomber_timer(int(self.bomb_rate_miliseconds))
        else:
            self.set_bomber_timer(0)


def main():
    # Every Pygame program has the following:
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, DOUBLEBUF | HWSURFACE)
    fpsClock = pygame.time.Clock()

    background = pygame.Surface((SCREENRECT.size))
    background.fill(AQUA)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Sprites
    all = pygame.sprite.OrderedUpdates()
    bomb = pygame.sprite.Group()
    bomber = pygame.sprite.Group()
    Bomb.containers = all, bomb
    Bomber.containers = all, bomber

    bomber = Bomber()
    bomber.set_bomber_timer(3000)

    # All games are essentially one giant loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit
                sys.exit()
            if event.type == DROP_BOMB:
                bomber.drop_bomb()

        all.clear(screen, background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
