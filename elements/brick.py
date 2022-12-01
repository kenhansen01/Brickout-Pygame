import pygame
from brickout.constants import *

from .base import BaseObject

class Brick(BaseObject):
    def __init__(self, brick_type, pos, groups, obstacles, width, height):
        super(Brick, self).__init__()
        self.type = brick_type
        self.pos = pos
        self.health = int(self.type)
        self.color = COLOR_LEGEND[self.type]
        self.image = pygame.Surface((width, height))
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.pos)
        self.old_rect = self.rect.copy()
        self.groups = groups
        self.obstacles = obstacles

    def update(self):
        self.old_rect = self.rect.copy()
        self.color = COLOR_LEGEND[self.type]
        self.image.fill(self.color)
        self.rect = self.image.get_rect(topleft=self.pos)

    def damage(self):
        if self.health > 0:
            self.health -= 1
            self.type = str(self.health)

        if self.health == 0:
            self.kill()


def damage_brick(brick):
    if brick.health > 0:
        brick.health -= 1
        brick.type = str(brick.health)

    if brick.health == 0:
        brick.kill()
