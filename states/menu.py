import pygame
from brickout.constants import *

from .base import BaseState
from sfx import SoundEffect

class Menu(BaseState):
    def __init__(self, title="Brickout Menu", credits=None, score=None, instructions="Use arrow keys to select an option and enter to select.", options=["Start game", "Quit game"]):
        super(Menu, self).__init__()
        # Sounds
        self.navigation_sound = SoundEffect(NAVIGATION_SOUND)
        self.confirm_sound = SoundEffect(CONFIRM_SOUND)
        
        # Text colors
        self.color = pygame.Color("white")
        self.a_color = pygame.Color("red")
        self.t_font = pygame.font.Font(None, 40)
        
        # Title, credits, score and instructions
        self.t_text = title
        self.c_text = credits
        self.s_text = score
        self.i_text = instructions
        self.title = self.t_font.render(self.t_text, True, self.color)
        self.t_rect = self.title.get_rect(center=(self.window_rect.centerx, TOP_OFFSET*2))
        self.credits = None if credits == None else self.font.render(self.c_text, True, self.color)
        self.c_rect = self.t_rect if credits == None else self.credits.get_rect(center=(self.window_rect.centerx, self.t_rect.bottom + 24))
        self.score = None if score == None else self.font.render(self.s_text, True, self.color)
        self.s_rect = self.c_rect if score == None else self.score.get_rect(center=(self.window_rect.centerx, self.c_rect.bottom + 24))
        self.instructions = self.font.render(self.i_text, True, self.color)
        self.i_rect = self.instructions.get_rect(center=(self.window_rect.centerx, self.s_rect.bottom + 24))
        
        # Options
        self.active_index = 0
        self.options = options
        self.next_state = "GAMEPLAY"
        self.level = 1

    def render_option(self, index):
        color = self.a_color if index == self.active_index else self.color
        return self.font.render(self.options[index], True, color)

    def get_option_position(self, text, index):
        remaining_height = HEIGHT - self.i_rect.bottom
        center = (self.window_rect.centerx, remaining_height + index * 50)
        return text.get_rect(center=center)

    def handle_action(self):
        if self.active_index == 0:
            self.confirm_sound.play()
            self.done = True

        elif self.active_index == 1:
            self.quit = True

    def get_event(self, event):
        if event.type == pygame.QUIT:
            self.quit = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.active_index = 1 if self.active_index <= 0 else 0
                self.navigation_sound.play()

            elif event.key == pygame.K_DOWN:
                self.active_index = 0 if self.active_index >= 1 else 1
                self.navigation_sound.play()

            elif event.key == pygame.K_RETURN:
                self.handle_action()

    def draw(self, window):
        window.fill(pygame.Color("black"))
        window.blit(self.title, self.t_rect)
        if not self.c_text == None:
            window.blit(self.credits, self.c_rect)
        if not self.s_text == None:
            window.blit(self.score, self.s_rect)
        window.blit(self.instructions, self.i_rect)

        for index, option in enumerate(self.options):
            option_render = self.render_option(index)
            window.blit(option_render, self.get_option_position(option_render, index))

class GameOver(Menu):
    def __init__(self, title="Game over", credits=None, score="Your current score is ", options=["New game", "Main menu"]):
        super(GameOver, self).__init__(title=title, credits=credits, score=score, options=options)
        self.persistent_info = {}

    def startup(self, persistent):
        self.persistent_info["score"] = persistent["score"]
        self.persistent_info["status"] = persistent["status"]
        self.persistent_info["level"] = persistent["level"]

        if self.persistent_info["status"] == "loser":
            self.s_text = f"Your final score was {self.persistent_info['score']} points"
            self.score = self.font.render(self.s_text, True, self.color)
            self.s_rect = self.score.get_rect(center=(self.window_rect.centerx, self.c_rect.bottom + 24))

        if self.persistent_info["status"] == "winner":
            self.t_text = f"Level {self.persistent_info['level']} complete"
            self.title = self.t_font.render(self.t_text, True, self.color)
            self.t_rect = self.title.get_rect(center=(self.window_rect.centerx, TOP_OFFSET*2))

            self.s_text = f"Your score is {self.persistent_info['score']} points"
            self.score = self.font.render(self.s_text, True, self.color)
            self.s_rect = self.score.get_rect(center=(self.window_rect.centerx, self.c_rect.bottom + 24))
            self.options=["Continue game", "Main menu"]
    
    def handle_action(self):
        if self.active_index == 0:
            self.confirm_sound.play()
            self.next_state = "GAMEPLAY"
            self.persist["reset"] = False if self.persistent_info["status"] == "winner" else True
            self.done = True

        elif self.active_index == 1:
            self.confirm_sound.play()
            self.persist["reset"] = True
            self.next_state = "MENU"
            self.done = True

class Credits(GameOver):
    def __init__(self):
        super(Credits, self).__init__(title="Congratulations, you've beaten the game!", credits="Pygame Brickout made by Ken Hansen using PyGame. Much thanks to Guilherme Juventino for a lot of borrowed code.", score="Your final score was ")
    
    def startup(self, persistent):
        self.persistent_info["score"] = persistent["score"]
        self.s_text = f"Your final score was {self.persistent_info['score']} points"
        self.score = self.font.render(self.s_text, True, self.color)
        self.s_rect = self.score.get_rect(center=(self.window_rect.centerx, self.c_rect.bottom + 24))