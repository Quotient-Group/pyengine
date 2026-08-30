'''Each animation has an id and a variant, both strings'''


import pygame


ANIMATIONS = {
    "player": {
        "idle": [
            pygame.image.load("assets/animations/player/idle/idle0.png").convert_alpha(),
            pygame.image.load("assets/animations/player/idle/idle1.png").convert_alpha(),
        ],
        "run": [
            pygame.image.load("assets/animations/player/run/run0.png").convert_alpha(),
            pygame.image.load("assets/animations/player/run/run1.png").convert_alpha(),
        ]
    }
}


def get_animation(id: str, variant: str):
    return ANIMATIONS[id][variant]
