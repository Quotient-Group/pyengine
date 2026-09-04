'''
There is a GUIElement class which holds a parent GUIElement instance (which is None for root) and a uv_rect: a numpy array of the form
(x,y,width,height), but with uv coordinates, so that everything scales smoothly in case of different resolutions.

Look at the rest of the documentation for better overview of specific elements
'''

from __future__ import annotations

import pygame
import numpy as np

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game import Game

from state import *
from tween import *
from utils import *


class GUIElement(StateObject, TweenObject):
    '''A GUIElement is a class that holds a parent GUIElement (which can be None) and a uv rectangle which represent proportions instead
    of direct quantities. The get_root_uv_rect method returns the proportions relative to the root node, otherwise the uv_rect refers to
    the proportions relative to the parent node.
    '''
    def __init__(self, parent: GUIElement | None = None, uv_rect: np.ndarray = np.array([0.0,0.0,0.0,0.0])):
        super().__init__()
        self.game: Game = None
        if parent:
            self.game = parent.game

        self.default_uv_rect = np.array(uv_rect)
        self.current_uv_pivot_point = (0.5,0.5)

        self.parent: GUIElement = parent
        self.uv_rect: np.ndarray = np.array(uv_rect)


    def shapeshift_to(self, target: tuple[float,float,float,float], duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Interpolates the element's uv_rect to the specified target'''
        self.change_to(value=self.uv_rect, dest=np.array(target), duration=duration, easing_func=easing_func, on_end=on_end)


    def rescale_to(self, target_size: tuple[float,float] = None, uv_pivot_point: tuple[float,float] = None, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Rescales the GUIElement to a certain target size around a pivot point whose uv represent its position _inside_ the uv_rect
        (for instance the point (0.5,0.5) is the center, while (0.0,0.0) is the origin. (1.0,1.0) is the bottom left etc)'''

        if not uv_pivot_point:
            uv_pivot_point = self.current_uv_pivot_point
        else:
            self.current_uv_pivot_point = uv_pivot_point

        # Let's compute the final rectangle, and then shapeshift ouselves to it. Start by the current uv_rect
        target = self.uv_rect

        # calculate the uv coords of the pivot point in the outer reference frame (the one of the parent)
        outer_uv_pivot_point = self.uv_rect[:2]+np.array(uv_pivot_point)*self.uv_rect[2:]

        # calculate the final position of the uv_rect
        final_uv_pos = -np.array(target_size)*np.array(uv_pivot_point) + outer_uv_pivot_point

        # calculate the target and shapeshift to it
        target = np.concatenate((final_uv_pos, np.array(target_size)))
        self.shapeshift_to(target=target, duration=duration, easing_func=easing_func, on_end=on_end)


    def scale_by(self, factor: float = 1.0, uv_pivot_point: tuple[float,float] = None, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Scale the GUIElement by some factor, around a pivot point whose uv represent its position _inside_ the uv_rect (for instance
        the point (0.5,0.5) is the center, while (0.0,0.0) is the origin. (1.0,1.0) is the bottom left etc)'''

        self.rescale_to(target_size=factor*np.array(self.uv_rect[2:]), uv_pivot_point=uv_pivot_point, duration=duration, easing_func=easing_func, on_end=on_end)


    def scale_to_default(self, uv_pivot_point: tuple[float,float] = None, duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        self.rescale_to(target_size=self.default_uv_rect[2:], uv_pivot_point=uv_pivot_point, duration=duration, easing_func=easing_func, on_end=on_end)


    def get_parent(self):
        '''Returns the parent GUIElement'''
        return self.parent


    def get_root_uv_rect(self):
        '''Returns the uv_rect relative to the root'''
        if self.parent is None:
            return self.uv_rect
        parent_rect = self.parent.get_root_uv_rect()
        parent_pos, parent_size = parent_rect[:2], parent_rect[2:]
        uv_pos, uv_size = self.uv_rect[:2], self.uv_rect[2:]

        pos = parent_pos + parent_size*uv_pos
        size = parent_size*uv_size

        return np.array((*pos, *size,))


    def get_rect(self, parent_surface: pygame.Surface):
        return self.get_root_uv_rect()*np.array(2*(*parent_surface.get_size(),))


class Container(GUIElement):
    '''
    A Container is a GUIElement with a list of children, to be updated and drawn during its sole default state (may be updated in future)
    '''
    def __init__(self, parent = None, uv_rect = np.array([0.0,0.0,1.0,1.0]), texture: pygame.Surface = None):
        super().__init__(parent, uv_rect)

        self.children: list = []

        self.color = GREEN
        self.texture = texture
        
        self.set_state(self.default)

    @state
    def default(self):
        def update(dt):
            for child in self.children.copy():
                child.update(dt)
        def draw(surface: pygame.Surface):
            if not isinstance(self, Root):
                if not self.texture:
                    pygame.draw.rect(surface=surface, color=self.color, rect=self.get_rect(parent_surface=surface))
                else:
                    final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(parent_surface=surface)[2:])
                    surface.blit(final_tex, dest=self.get_rect(parent_surface=surface))
            for child in self.children:
                child.draw(surface)

        return update, draw


    def add_child(self, cls, *args, **kwargs):
        kwargs["parent"] = self
        self.children.append(cls(*args, **kwargs))


    def clear(self):
        for child in self.children:
            del child
        self.children.clear()


    def set_color(self, color: pygame.Color = None):
        if color:
            self.color = color


class Root(Container):
    '''
    A Root is a special Container with None as parent and fixed uv_rect (0.0,0.0,1.0,1.0). 
    '''
    def __init__(self, game: Game = None):
        super().__init__(parent=None, uv_rect=np.array([0.0,0.0,1.0,1.0]))
        self.game: Game = game


class Button(GUIElement):
    def __init__(self, parent = None, uv_rect = np.array([0, 0, 0, 0]), texture: pygame.Surface = None, at_click: function = lambda: None):
        super().__init__(parent, uv_rect)

        self.color: pygame.Color = pygame.Color(0,0,255,255)
        self.is_active = False

        self.texture: pygame.Surface = texture

        self.tick_sound = pygame.mixer.Sound("assets/sounds/tick_0.ogg")
        self.select_sound = pygame.mixer.Sound("assets/sounds/select_0.ogg")

        self.at_click: function = at_click

        self.set_state(self.inactive)

    @state
    def active(self):
        def update(dt):
            if not self.is_active:
                self.new_tween_stream()
                self.scale_to_default(duration=0.05, easing_func=ease_out_quad)
                self.set_state(self.inactive)
            if self.game.click:
                self.set_state(self.clicked)
        def draw(surface: pygame.Surface):
            self.set_active(pygame.Rect(self.get_rect(surface)).collidepoint(self.game.mpos))

            if not self.texture:
                final_tex = pygame.Surface(size=self.get_rect(parent_surface=surface)[2:])
                final_tex.fill(color=self.color)
            else:
                final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(parent_surface=surface)[2:])
            surface.blit(final_tex, dest=self.get_rect(parent_surface=surface))

        return update, draw

    @state
    def clicked(self):
        self.select_sound.play()
        self.at_click()
        self.new_tween_stream()
        self.scale_to_default(duration=0.05, easing_func=ease_out_quad)
        self.do(lambda: self.set_state(self.active))
        self.do(lambda: self.scale_by(factor=1.1, duration=0.05, easing_func=ease_out_quad))
        def update(dt):
            ...
        def draw(surface: pygame.Surface):
            if not self.texture:
                final_tex = pygame.Surface(size=self.get_rect(parent_surface=surface)[2:])
                final_tex.fill(color=self.color)
            else:
                final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(parent_surface=surface)[2:])
            surface.blit(final_tex, dest=self.get_rect(parent_surface=surface))

        return update, draw

    @state
    def inactive(self):
        def update(dt):
            if self.is_active:
                self.tick_sound.play()
                self.new_tween_stream()
                self.scale_by(factor=1.1, duration=0.05, easing_func=ease_out_quad)
                self.set_state(self.active)
        def draw(surface: pygame.Surface):
            self.set_active(pygame.Rect(self.get_rect(surface)).collidepoint(self.game.mpos))

            if not self.texture:
                final_tex = pygame.Surface(size=self.get_rect(parent_surface=surface)[2:])
                final_tex.fill(color=self.color)
            else:
                final_tex = pygame.transform.scale(surface=self.texture, size=self.get_rect(parent_surface=surface)[2:])
            surface.blit(final_tex, dest=self.get_rect(parent_surface=surface))

        return update, draw


    def set_active(self, state=False):
        self.is_active = state
