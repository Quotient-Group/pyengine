
import pygame
from pathlib import Path


MODULE_DIR = Path(__file__).parent
ANIMATIONS_DIR = MODULE_DIR / "animations"



'''Each animation has an id and a variant, both strings'''


ANIMATIONS = {
    "player": {
        "idle": [
            pygame.image.load(str(ANIMATIONS_DIR / "player/idle/idle0.png")).convert_alpha(),
            pygame.image.load(str(ANIMATIONS_DIR / "player/idle/idle1.png")).convert_alpha(),
        ],
        "run": [
            pygame.image.load(str(ANIMATIONS_DIR / "player/run/run0.png")).convert_alpha(),
            pygame.image.load(str(ANIMATIONS_DIR / "player/run/run1.png")).convert_alpha(),
        ]
    }
}


def get_animation(id: str, variant: str):
    return ANIMATIONS[id][variant]
