import pygame

from states import Splash, GamePlay

from .constants import *

class Brickout(object):
    def __init__(self, start_state) -> None:
        self.done = False
        self.window = None
        self.clock = None
        self.fps = None
        self.states = None
        self.state_name = start_state
        self.state = None
        self._init_pygame()

    def _init_pygame(self):
        pygame.init()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        # Game states
        self.states = {
            "SPLASH": Splash(),
            "GAMEPLAY": GamePlay()
        }

        # Game start
        self.done = False
        self.clock = pygame.time.Clock()
        self.fps = FPS
        self.state = self.states[self.state_name]

    # TODO: def _flip_state to advance through screens
    def _flip_state(self):
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)
    
    def _event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def _draw(self):
        self.state.draw(self.window)

    def _update(self, dt):
        if self.state.quit:
            self.done = True
        
        # TODO: elif to change state
        elif self.state.done:
            self._flip_state()

        self.state.update(dt)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self._event_loop()
            self._update(dt)
            self._draw()
            pygame.display.update()