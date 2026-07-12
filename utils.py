
import pygame
import inspect


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
