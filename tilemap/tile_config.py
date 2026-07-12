
import pygame
from pathlib import Path


MODULE_DIR = Path(__file__).parent
IMAGES_DIR = MODULE_DIR / "images"


'''
For each tile there are multiple variants. You use the TILES dictionary for multiple purposes:
to retrieve the ids, to know how many variants are there for each id, or to retrieve the textures.
Each of these things has its own function below.
'''

TILES = {
    "stone": [
        pygame.image.load(str(IMAGES_DIR / "stone/stone4.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone1.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone2.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone3.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone4.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone5.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone6.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone7.png")).convert_alpha(),
        # pygame.image.load(str(IMAGES_DIR / "stone/stone8.png")).convert_alpha(),
    ],

    "grass": [
        pygame.image.load(str(IMAGES_DIR / "grass/grass4.png")).convert_alpha(),
    ]
}

def get_tile_id(index: int) -> str:
    return list(TILES.keys())[index%len(TILES.keys())]

def get_tile_index(id: str) -> int:
    return list(TILES.keys()).index(id)

def get_tile_texture(id: str, variant: int) -> pygame.Surface:
    return TILES[id][variant]

def get_number_of_variants(id: str):
    return len(TILES[id])
