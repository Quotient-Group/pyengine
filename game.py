
import pygame
import sys
import numpy as np
import time

from state import *
from tween.tween import *
from tween.easing_funcs import *
from gui.gui import *
from tilemap.tilemap import TilemapManager
from entity.player import Player
from utils import *


class Game(StateObject, TweenObject):
    def __init__(self, display: pygame.Surface, screen_res: tuple[int,int]):
        super().__init__()

        self.display: pygame.Surface = display
        self.screen_res = screen_res
        self.gui_manager = GUIManager(game=self)

        self.mpos = np.array(pygame.mouse.get_pos())
        self.click = pygame.mouse.get_just_pressed()

        self.window = pygame.Surface(screen_res)
        self.window_pos = np.array([0,0])

        self.prev_time = time.time()

        self.camera_offset: np.ndarray = np.array([0.0,0.0])

        self.tilemap_manager = TilemapManager()
        self.tilemap_manager.load("testmap")

        self.player = Player()

        self.set_state(self.intro)

    @state
    def intro(self):
        self.set_display(res=(1920,1080))

        image = pygame.image.load("title.png").convert()
        image.set_alpha(0)
        image = pygame.transform.smoothscale(surface=image, size=self.window.get_size())
        self.wait(duration=0.5)
        self.fade_in_out(surface=image, duration_in=1.0, duration=2.0, duration_out=1.0)
        self.do(lambda: self.set_state(self.main_menu))
        def update(dt):
            ...
        def draw():
            self.window.fill((0,0,0))
            self.window.blit(image)

        return update, draw

    @state
    def main_menu(self):
        self.set_display(res=(1920,1080))

        pygame.mixer.music.load("music.ogg")
        pygame.mixer.music.play(-1, fade_ms=5000)
        pygame.mixer.music.set_volume(0.5)

        background = pygame.image.load(file="background_3.png").convert()
        background = pygame.transform.smoothscale(surface=background, size=self.window.get_size())

        table_tex = pygame.image.load("table.png").convert_alpha()
        play_tex = pygame.image.load("play.png").convert_alpha()
        exit_tex = pygame.image.load("exit.png").convert_alpha()

        self.gui_manager.add_element(cls=Container, uv_rect=(0.3225,0.1,0.355,0.8), texture=table_tex)
        self.gui_manager.add_element(cls=Button, uv_rect=(0.22,0.35,0.56,0.116), texture=play_tex, at_click=lambda: self.set_state(self.test))
        self.gui_manager.add_element(cls=Button, uv_rect=(0.22,0.5,0.56,0.116), texture=exit_tex, at_click=lambda: self.set_state(self.exit))

        self.fade_in(self.window, duration=3.0)

        def update(dt):
            self.gui_manager.update(dt)
        def draw():
            # self.window.fill((0,0,0))
            self.window.blit(background)
            self.gui_manager.draw(self.window)

        return update, draw

    @state
    def new_game(self):
        ...
    
    @state
    def load_game(self):
        ...
    
    @state
    def options(self):
        ...

    @state
    def exit(self):
        self.new_tween_stream()
        self.wait(duration=0.25)
        self.do(lambda: pygame.quit())
        self.do(lambda: sys.exit())

        return lambda dt: None, lambda: None

    @state
    def test(self):
        self.set_display(res=(640,360))
        def update(dt):
            target_pos = self.player.pos - np.array(self.display.get_size())/2
            self.camera_offset += (target_pos-self.camera_offset)*1.5*dt
            
            if pygame.key.get_just_pressed()[pygame.K_ESCAPE]:
                self.set_state(self.intro)
                return
            self.player.update(dt)

        def draw():
            self.window.fill((0,0,0))

            self.tilemap_manager.draw(self.window, self.camera_offset)
            self.player.draw(self.window, self.camera_offset)

        return update, draw


    def set_display(self, res=(1920,1080), flags=pygame.SCALED | pygame.FULLSCREEN):
        self.display = pygame.display.set_mode(get_nearest_res(target=res, res=self.screen_res), flags=flags if flags else 0)
        self.window = pygame.Surface(self.display.get_size())


    def update(self):
        dt = time.time()-self.prev_time
        self.prev_time = time.time()

        self.mpos = np.array(pygame.mouse.get_pos())
        self.click = pygame.mouse.get_just_pressed()

        super().update(dt)


    def draw(self, display: pygame.Surface = None):
        display.fill((0,0,0))
        super().draw()
        display.blit(self.window, self.window_pos)


    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update()
            self.draw(self.display)
            pygame.display.flip()
