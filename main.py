
import pygame
import sys
from utils import *

pygame.init()
pygame.mixer.init()

info = pygame.display.Info()

SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT

WIDTH, HEIGHT = get_nearest_res(target=(640,480), res=SCREEN_RES)
RESOLUTION = (WIDTH, HEIGHT)

display = pygame.display.set_mode(RESOLUTION, pygame.SCALED | pygame.FULLSCREEN)

if len(sys.argv) > 1:
    if sys.argv[1] == "-e":
        from tilemap.map_editor import MapEditor

        map_editor = MapEditor(RESOLUTION)
        map_editor.run(display=display)

from game import Game

# pygame.mouse.set_visible(False)

game = Game(display=display, screen_res=SCREEN_RES)
game.run()
