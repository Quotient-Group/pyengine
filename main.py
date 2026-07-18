
import pygame
import sys
from utils import get_nearest_res

pygame.init()
info = pygame.display.Info()

SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
SCREEN_RES = SCREEN_WIDTH, SCREEN_HEIGHT

WIDTH, HEIGHT = get_nearest_res(target=(640,480), res=SCREEN_RES)
RESOLUTION = (WIDTH, HEIGHT)

DISPLAY = pygame.display.set_mode(RESOLUTION, pygame.SCALED | pygame.FULLSCREEN)

if len(sys.argv) > 1:
    if sys.argv[1] == "-e":
        from tilemap.map_editor import MapEditor

        map_editor = MapEditor(RESOLUTION)
        map_editor.run(DISPLAY)

from game import Game

game = Game(RESOLUTION)
game.run(DISPLAY)
