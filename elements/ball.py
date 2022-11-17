import pygame
from math import sqrt

from brickout.constants import *
from .base import BaseObject

# Import blocks and other elements


class Ball(BaseObject):
    def __init__(self, groups, obstacles, player, surf_rect):
        super(Ball, self).__init__()
        
        self.surf_rect = surf_rect
        self.color = pygame.Color("lightblue")
        self.ball_sq_l = int(B_RADIUS * sqrt(2))
        self.rect = pygame.Rect((WIDTH - self.ball_sq_l)/2, HEIGHT // 2, self.ball_sq_l, self.ball_sq_l)
        self.old_rect = self.rect.copy()
        self.speed_x = 0
        self.speed_y = 0
        self.speed = 5
        self.active = False
        self.aim = "right"
        self.groups = groups
        self.obstacles = obstacles
        self.player = player

    def update(self):
        # Previous frame
        self.old_rect = self.rect.copy()

        # Current frame (x, y positions)

        if self.active:
            self.rect.x += self.speed_x
            # self.collision("horizontal")
            # self.collision_window("horizontal")
            self.rect.x = round(self.rect.x)

            self.rect.y += self.speed_y
            # self.collision("vertical")
            # self.collision_window("vertical")
            self.rect.y = round(self.rect.y)

        if not self.active:
            # Sticking the ball to the player pad
            self.rect.centerx = self.player.rect.centerx
            self.rect.bottom = self.player.rect.top

            # Aiming the ball
            if self.player.keystate[pygame.K_LEFT] and not self.player.keystate[pygame.K_RIGHT]:
                self.aim = "left"

            if self.player.keystate[pygame.K_RIGHT] and not self.player.keystate[pygame.K_LEFT]:
                self.aim = "right"

            # Shooting the ball
            if self.player.keystate[pygame.K_SPACE]:

                if self.aim == "left":
                    self.speed_x = -self.speed
                    self.speed_y = -self.speed

                elif self.aim == "right":
                    self.speed_x = self.speed
                    self.speed_y = -self.speed

                self.active = True

    def reset_ball(self):
        if self.player.lives > 0:
            self.player.lives -= 1

            if self.player.lives != 0:
                self.active = False

    def draw(self, window):
        pygame.draw.circle(window, (self.color.r, self.color.g, self.color.b), (self.rect.center), B_RADIUS)