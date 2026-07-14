
import pygame
import sys
import numpy as np
import time

from state import *
from tween.tween import *
from tween.easing_funcs import *
from tilemap.tilemap import TilemapManager
from entity.player import Player
from utils import *


class Game(StateObject, TweenObject):
    def __init__(self, resolution: tuple[int,int]):
        super().__init__()

        self.window = pygame.Surface(resolution)
        self.window_pos = np.array([0,0])

        self.prev_time = time.time()

        self.camera_offset: np.ndarray = np.array([0,0])

        self.tilemap_manager = TilemapManager()
        self.tilemap_manager.load("testmap")

        self.set_state(self.main_menu)

        self.player = Player()


    def set_state(self, state: function):
        self.state_manager.set_state(state)


    @state
    def intro(self):
        image = pygame.image.load("scemo.png").convert()
        image.set_alpha(0)
        self.wait(duration=0.5)
        self.fade_in_out(image, duration_in=1.0, duration=2.0, duration_out=1.0)
        self.do(lambda: self.set_state(self.main_menu))
        def update(dt):
            ...
        def draw():
            self.window.fill((0,0,0))
            self.window.blit(image)

        return update, draw


    @state
    def main_menu(self):
        goku = pygame.image.load("goku.png").convert()
        pos = np.array([100.0,0.0])
        self.move_by(value=pos, shift=np.array([300.0,400.0]), duration=1.0, easing_func=ease_in_out_quad)
        self.move_by(value=pos, shift=np.array([100.0,0.0]), duration=1.0, easing_func=ease_in_out_quad)
        def update(dt):
            ...
        def draw():
            self.window.fill((0,0,0))
            self.window.blit(goku, pos)

        return update, draw


    @state
    def test(self):
        def update(dt):
            if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
            self.player.update(dt)

        def draw():
            self.tilemap_manager.draw(self.window, self.camera_offset)
            self.player.draw(self.window, self.camera_offset)

        return update, draw


    def update(self):
        dt = time.time()-self.prev_time
        self.prev_time = time.time()

        super().update(dt)


    def draw(self, display: pygame.Surface = None):
        super().draw()
        display.blit(self.window, self.window_pos)


    def run(self, display: pygame.Surface = None):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw(display)
            pygame.display.flip()
