
import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 640, 480
RESOLUTION = (WIDTH, HEIGHT)

DISPLAY = pygame.display.set_mode(RESOLUTION)

if len(sys.argv) > 1:
    if sys.argv[1] == "-e":
        from tilemap.map_editor import MapEditor

        map_editor = MapEditor(RESOLUTION)
        map_editor.run(DISPLAY)

from game import Game

game = Game(RESOLUTION)
game.run(DISPLAY)
