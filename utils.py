
import pygame
import inspect
import win32con, win32gui, win32print
import math


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
