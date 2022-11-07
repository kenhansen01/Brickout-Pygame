import pygame
from brickout.constants import *

from .base import BaseObject

class Player(BaseObject):
    def __init__(self, groups, obstacles):
        super(Player, self).__init__()
        self.x = WIDTH / 2
        self.y = HEIGHT - P_HEIGHT - 5
        self.speed = 6
        self.speed_x = 0
        
        # Define the player image
        self.rect = pygame.Rect((0, 0), (P_WIDTH, P_HEIGHT))
        self.rect.center = (self.x, self.y)
        self.color = pygame.Color("white")
        self.image = pygame.Surface((self.rect.width, self.rect.height))
        self.image.fill(self.color)
        
        # old_rect used for movement
        self.old_rect = self.rect.copy()
        
        # Sprite groups
        self.groups = groups
        self.obstacles = obstacles
        
        # Default lives and score
        self.lives = 3
        self.score = 0

    def update(self):
        # Previous frame
        self.old_rect = self.rect.copy()

        self.keystate = pygame.key.get_pressed()

        # Handling player movement
        if self.keystate[pygame.K_LEFT] and not self.keystate[pygame.K_RIGHT]:
            self.speed_x = -self.speed

        elif self.keystate[pygame.K_RIGHT] and not self.keystate[pygame.K_LEFT]:
            self.speed_x = self.speed

        else:
            self.speed_x = 0

        # Current frame (x position)
        self.rect.x += self.speed_x

        # Preventing player from leaving the screen
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH

        elif self.rect.left <= 0:
            self.rect.left = 0

        # Setting max score
        if self.score > 9999999:
            self.score = 9999999
