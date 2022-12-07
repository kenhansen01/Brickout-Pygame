import pygame
from brickout.constants import *
from random import randint, randrange

class Star(pygame.sprite.Sprite):
    def __init__(self, position):
        super(Star, self).__init__()
        self.color = (randint(1, 255), randint(1, 255), randint(1, 255))
        self.image = pygame.Surface((randint(2, 3), randint(2, 3)))
        self.image.fill(self.color)
        self.rect = self.image.get_rect()
        self.x = position[0]
        self.y = position[1]
        self.speed = randrange(1, 3)
        self.rect.center = (self.x, self.y)

    def update(self):
        self.rect.y += self.speed

        if self.rect.top >= HEIGHT:
            self.kill()

    def draw(self, window):
        pygame.draw.rect(window, self.color, self.rect, self.rect.width)


class StarField:
    def __init__(self):
        self.stars = []
        self.amount = randint(5, 8)
        self.timer = randrange(1, 10)

        for i in range(self.amount):
            self.stars.append(Star((randint(0, WIDTH), randrange(TOP_OFFSET, TOP_OFFSET + 2))))

    def update(self):
        self.timer -= 1

        for star in self.stars:
            star.update()

        if self.timer == 0:
            self.timer = randrange(1, 10)

            self.stars.append(Star((randint(0, WIDTH), randrange(TOP_OFFSET, TOP_OFFSET + 2))))

    def draw(self, window):
        for star in self.stars:
            star.draw(window)