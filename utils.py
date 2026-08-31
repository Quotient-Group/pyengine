
import pygame
import inspect
import math

'''Useful variables'''
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_GRAY = (192, 192, 192)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
PINK = (255, 192, 203)
BROWN = (165, 42, 42)
OLIVE = (128, 128, 0)
TEAL = (0, 128, 128)
NAVY = (0, 0, 128)
MAROON = (128, 0, 0)
GOLD = (255, 215, 0)
CORAL = (255, 127, 80)
INDIGO = (75, 0, 130)
VIOLET = (238, 130, 238)
HOT_PINK = (255, 105, 180)
CRIMSON = (220, 20, 60)
CHOCOLATE = (210, 105, 30)
TURQUOISE = (64, 224, 208)
LAVENDER = (230, 230, 250)
PLUM = (221, 160, 221)
KHAKI = (240, 230, 140)
SALMON = (250, 128, 114)
TOMATO = (255, 99, 71)
ORANGE_RED = (255, 69, 0)
DARK_GOLDENROD = (184, 134, 11)
LIME_GREEN = (50, 205, 50)
FOREST_GREEN = (34, 139, 34)
SKY_BLUE = (135, 206, 235)


'''
Useful functions
'''

# Returns a surface with alpha regulation
def AlphaSurface(size: tuple[int,int] = (32,32), alpha: int = 50) -> pygame.Surface:
    alpha_surface = pygame.Surface(size)
    alpha_surface.set_alpha(alpha)
    return alpha_surface

# Checks if a function accepts a certain parameter as kwarg
def accepts_kwarg(func, kwarg_name):
    func = inspect.unwrap(func)
    sig = inspect.signature(func)
    for param in sig.parameters.values():
        if param.kind == inspect.Parameter.VAR_KEYWORD:
            return True
        if param.name == kwarg_name:
            # Ensure it's not positional-only
            if param.kind != inspect.Parameter.POSITIONAL_ONLY:
                return True
    return False


def get_nearest_res(target: tuple[int,int], res: tuple[int,int]):
    GCD = math.gcd(res[0], res[1])
    candidates = [(res[0]/d, res[1]/d) for d in range(1, GCD+1)]
    def score(candidate: tuple[int,int]):
        return abs(math.hypot(*candidate) - math.hypot(*target))
    favorite = candidates[0]
    for candidate in candidates:
        if candidate[0]==int(candidate[0]) and candidate[1]==int(candidate[1]):
            if score(candidate) < score(favorite):
                favorite = candidate
    return (int(favorite[0]), int(favorite[1]))
