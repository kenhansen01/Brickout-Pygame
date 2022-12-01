import pygame
from brickout.constants import *

from .levels import LEVELS
from elements import Brick

def level_setup(groups, obstacles, level=1):
    # Cycle through all rows and columns in LEVEL
    brick_group = pygame.sprite.Group()

    brick_map = LEVELS[level - 1]

    brick_width = WIDTH / len(brick_map[0]) - GAP_SIZE
    brick_height = HEIGHT / len(brick_map) - 35 - GAP_SIZE

    for row_index, row in enumerate(brick_map):
        for col_index, col in enumerate(row):

            if col != " ":
                # Find the x and y position of each individual brick
                x = col_index * (brick_width + GAP_SIZE) + GAP_SIZE // 2
                y = TOP_OFFSET + row_index * (brick_height + GAP_SIZE) + GAP_SIZE // 2
                brick = Brick(col, (x, y), groups, obstacles, brick_width, brick_height)
                brick_group.add(brick)

    return brick_group