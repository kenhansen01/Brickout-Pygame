import pygame
from brickout.constants import *

# Import game elements

# Import base state
from .base import BaseState


class GamePlay(BaseState):
    def __init__(self):
        super(GamePlay, self).__init__()
        self.level = 1
        self.next_state = "SPLASH"  # Menu or Gameover
        self.reset = False

        # Determine if player lost or won
        self.status = ""

        # Used to pause game
        self.paused = False

        self.main_surface = pygame.Surface((WIDTH, HEIGHT))
        self.main_rect = self.main_surface.get_rect()

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collide_sprites = pygame.sprite.Group()
        # this will be replace by level_setup once that is built
        self.block_group = pygame.sprite.Group()

        # Instantiate Player, Ball Classes
        self.player = None
        self.ball = None

        # Text setup
        self.ui_font = pygame.font.Font(None, 40)
        self.score = 0  # replace with self.player.score
        self.score_text = self.ui_font.render(
            f"Score: {self.score}", True, pygame.Color("White"))
        self.score_rect = self.score_text.get_rect(center=(70, 25))

        self.lives = 3  # replace with self.player.lives
        self.lives_text = self.ui_font.render(
            f"Lives: {self.lives}", True, pygame.Color("White"))
        self.lives_rect = self.lives_text.get_rect(center=(1210, 25))

        self.paused_text = self.font.render(
            f"Paused", True, pygame.Color("White"))
        self.paused_rect = self.paused_text.get_rect(
            center=self.window_rect.center)

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        elif event.type == pygame.KEYUP and (event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN):

            if not self.paused:
                self.paused = True
            else:
                self.paused = False

    def startup(self, persistent):
        self.persist["score"] = 0

        if persistent:
            self.reset = persistent["reset"]

        # Reset player position

        # Reset ball status/position

        if self.status == "lost" or self.reset:
            # Resetting player score
            self.score = 0
            # set player score to 0

            # Resetting player lives
            self.lives = 3
            # set player lives to 3

            self.level = 1

        # Resetting the level
        if not self.block_group or self.status == "loser":
            self.all_sprites.empty()
            self.collide_sprites.empty()
            self.block_group.empty()

    def draw(self, window):
        window.fill(pygame.Color("black"))

        window.blit(self.main_surface, self.main_rect)

        self.main_surface.fill(pygame.Color("black"))

        # Drawing the game objects

        # Drawing the ui text
        window.blit(self.score_text, self.score_rect)
        window.blit(self.lives_text, self.lives_rect)

        if self.paused:
            window.blit(self.paused_text, self.paused_rect)

    def update(self, dt):
        if not self.paused:
            # Resetting main_surface to default position (required for screenshake)
            self.main_rect.topleft = (0, 0)

            # Updating the lives text
            self.lives = self.lives  # self.player.lives
            self.lives_text = self.ui_font.render(
                f"Lives: {self.lives}", True, pygame.Color("White"))

            # Updating the score text
            self.score = self.score  # self.player.score
            self.persist["score"] = self.score
            self.score_text = self.ui_font.render(
                f"Score: {self.score}", True, pygame.Color("White"))
