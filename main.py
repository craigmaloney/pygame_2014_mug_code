#!/usr/bin/env python
import sys
import pygame
import random
from pygame.locals import DOUBLEBUF
from pygame.locals import HWSURFACE
from pygame.locals import QUIT
from pygame.locals import SRCALPHA
from pygame.locals import USEREVENT
from pygame.locals import K_SPACE
from pygame.locals import KEYDOWN

SCREENRECT = pygame.Rect(0, 0, 800, 600)
FPS = 60
AQUA = (0, 255, 255)
LIGHT_GRAY = (200, 200, 200)
TRANSPARENT_FLOOR = (0, 0, 0, 0)
DARK_GRAY = (20, 20, 20)
DROP_BOMB = USEREVENT
CHANGE_DIRECTION = USEREVENT + 1
WAIT_EXPLOSION = USEREVENT + 2


class Floor(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 0
        self.y = SCREENRECT.size[1]
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((SCREENRECT.size[0], 100), SRCALPHA)
        self.image.fill(TRANSPARENT_FLOOR)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.speed = 0

    def update(self):
        self.y -= self.speed
        self.rect.topleft = (self.x, self.y)
        if self.y <= 0:
            self.y = SCREENRECT.size[1]
            self.speed = 0

    def explode_bombs(self):
        self.speed = 3


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
        if self.y >= SCREENRECT.size[1]:
            self.explode()

    def explode(self):
        # Have a magnificent explosion here
        self.kill()

    def stop_falling(self):
        self.speed = 0


class Bomber(pygame.sprite.Sprite):
    def __init__(self):
        self.x = 400
        self.y = 30

        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = pygame.Surface((50, 200))
        self.image.fill(LIGHT_GRAY)

        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.madness = 2
        self.alive_bombs = 0
        self.dropping_bombs = False
        self.waiting_for_reset = False

    def update(self):
        if self.dropping_bombs:
            self.x += self.dx
            if self.x > SCREENRECT.size[0] - 50:
                self.x = SCREENRECT.size[0] - 50
                self.dx *= -1
            if self.x < 50:
                self.x = 50
                self.dx *= -1
        self.rect.center = (self.x, self.y)

    def reset_game(self):
        self.madness = 2
        self.reset_level()

    def reset_level(self):
        self.num_bombs = self.set_num_bombs()
        self.alive_bombs = self.num_bombs
        self.speed = (self.madness / 2)
        self.bomb_rate_miliseconds = self.set_bomb_rate_miliseconds()
        self.dx = self.speed
        self.dropping_bombs = False
        self.change_direction()
        self.set_bomber_timer(int(self.bomb_rate_miliseconds))
        print "Starting game"

    def set_bomb_rate_miliseconds(self):
        brms = 1500 - (self.madness * 200)
        if brms <= 0:
            brms = 100
        return brms

    def set_num_bombs(self):
        return self.madness * 5

    def set_bomber_timer(self, rate):
        pygame.time.set_timer(DROP_BOMB, rate)

    def drop_bomb(self):
        Bomb(self.x, self.y, self.speed)
        self.num_bombs = self.num_bombs - 1
        if self.num_bombs > 0:
            self.dropping_bombs = True
            self.set_bomber_timer(int(self.bomb_rate_miliseconds))
        else:
            self.dropping_bombs = False
            self.set_bomber_timer(0)

    def change_direction(self):
        new_direction = random.randint(-1, 1)
        if new_direction != 0:
            self.dx = new_direction * self.speed
            pygame.time.set_timer(
                CHANGE_DIRECTION,
                0)
            pygame.time.set_timer(
                CHANGE_DIRECTION,
                int(self.bomb_rate_miliseconds / 2))

    def bomb_destroy(self):
        self.alive_bombs -= 1
        if self.alive_bombs <= 0:
            self.next_level()

    def next_level(self):
            self.madness += 1
            self.reset_level()

    def bomb_explode(self):
        # Muhahahaha! Got you! Stop everything!
        if self.waiting_for_reset is False:
            print "Resetting..."
            self.waiting_for_reset = True
            self.dropping_bombs = False
            self.dx = 0
            self.num_bombs = 0
            self.alive_bombs = 0
            pygame.time.set_timer(DROP_BOMB, 0)
            pygame.time.set_timer(CHANGE_DIRECTION, 0)
            # Wait 5 seconds for the bombs to be cleared
            pygame.time.set_timer(WAIT_EXPLOSION, 5 * 1000)

    def previous_level(self):
        print "Previous level"
        # Start from the previous level when player fails
        self.madness = self.madness - 1
        if self.madness <= 2:
            self.madness = 2
        self.waiting_for_reset = False
        pygame.time.set_timer(WAIT_EXPLOSION, 0)
        self.reset_level()


def main():
    # Every Pygame program has the following:
    pygame.init()
    screen = pygame.display.set_mode(SCREENRECT.size, DOUBLEBUF)
    fpsClock = pygame.time.Clock()

    background = pygame.Surface((SCREENRECT.size))
    background.fill(AQUA)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    # Sprites
    all = pygame.sprite.OrderedUpdates()
    bomb = pygame.sprite.Group()
    bomber = pygame.sprite.Group()
    floor = pygame.sprite.Group()
    Bomb.containers = all, bomb
    Bomber.containers = all, bomber
    Floor.containers = all, floor

    bomber_sprite = Bomber()
    floor_sprite = Floor()
    game_running = False

    # All games are essentially one giant loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit
                sys.exit()
            if event.type == DROP_BOMB:
                bomber_sprite.drop_bomb()
            if event.type == CHANGE_DIRECTION:
                bomber_sprite.change_direction()
            if event.type == WAIT_EXPLOSION:
                bomber_sprite.previous_level()
            if not game_running and \
                    (event.type == KEYDOWN and event.key == K_SPACE):
                game_running = True
                bomber_sprite.reset_game()

        bomb_floor = pygame.sprite.groupcollide(
            bomb,
            floor,
            False,
            False)
        if bomb_floor:
            bomber_sprite.bomb_explode()
            floor_sprite.explode_bombs()
            for bomb_sprite in bomb.sprites():
                print bomb_sprite
                bomb_sprite.stop_falling()
            for floor_bomb in bomb_floor:
                floor_bomb.explode()

        all.clear(screen, background)
        all.update()
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        fpsClock.tick(FPS)

if __name__ == "__main__":
    main()
