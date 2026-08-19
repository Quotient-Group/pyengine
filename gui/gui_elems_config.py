'''
There is a GUIElement class which holds a parent GUIElement instance (which is None for root) and a uv_rect: a numpy array of the form
(x,y,width,height), but with uv coordinates, so that everything scales smoothly in case of different resolutions.

Look at the rest of the documentation for better overview of specific elements
'''

import pygame
import numpy as np

from project.state import *
from project.tween.tween import *


class GUIElement(StateObject, TweenObject):
    '''A GUIElement is a class that holds a parent GUIElement (which can be None) and a uv rectangle which represent proportions instead
    of direct quantities. The get_root_uv_rect method returns the proportions relative to the root node, otherwise the uv_rect refers to
    the proportions relative to the parent node.
    '''
    def __init__(self, parent: GUIElement | None = None, uv_rect: np.ndarray = np.array([0.0,0.0,0.0,0.0])):
        super().__init__()

        self.parent: GUIElement = parent
        self.uv_rect: np.ndarray = uv_rect


    def shapeshift_to(self, target: tuple[float,float,float,float], duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Interpolates the element's uv_rect to the specified target'''
        self.move_to(value=self.uv_rect, dest=np.array(target), duration=duration, easing_func=easing_func, on_end=on_end)


    def scale_by(self, factor: float = 1.0, uv_pivot_point: tuple[float,float] = (0.5,0.5), duration=1.0, easing_func=lambda t: t, on_end=lambda: None):
        '''Scale the GUIElement by some factor, around a pivot point whose uv represent its position _inside_ the uv_rect (for instance
        the point (0.5,0.5) is the center, while (0.0,0.0) is the origin. (1.0,1.0) is the bottom left etc)'''

        # Let's compute the final rectangle, and then shapeshift ouselves to it. Start by the current uv_rect
        target = self.uv_rect

        # calculate the uv coords of the pivot point in the outer reference frame (the one of the parent)
        outer_uv_pivot_point_coords = self.uv_rect[:2]+np.array(uv_pivot_point)*self.uv_rect[2:]

        # calculate the final position of the uv_rect
        final_uv_pos = target[:2]-outer_uv_pivot_point_coords
        final_uv_pos = factor*final_uv_pos + outer_uv_pivot_point_coords

        # calculate the target and shapeshift to it
        target = np.concatenate((final_uv_pos, factor*self.uv_rect[2:]))
        self.shapeshift_to(target=target, duration=duration, easing_func=easing_func, on_end=on_end)


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


class Container(GUIElement):
    '''
    A Container is a GUIElement with a list of children, to be updated and drawn during its sole default state (may be updated in future)
    '''
    def __init__(self, parent = None, uv_rect = np.array([0.0,0.0,1.0,1.0])):
        super().__init__(parent, uv_rect)

        self.children: list = []

        self.color: pygame.Color = pygame.Color(0,0,0,0)
        
        self.set_state(self.default)

    @state
    def default(self):
        def update(dt):
            for child in self.children.copy():
                child.update(dt)
        def draw(surface: pygame.Surface):
            if not isinstance(self, Root):
                rect = self.get_root_uv_rect()*np.array(2*(*surface.get_size(),))
                pygame.draw.rect(surface=surface, color=self.color, rect=rect)
            for child in self.children:
                child.draw(surface)

        return update, draw


    def add_child(self, child: GUIElement):
        self.children.append(child)


    def set_color(self, color: pygame.Color = None):
        if color:
            self.color = color


class Root(Container):
    '''
    A Root is a special Container with None as parent and fixed uv_rect (0.0,0.0,1.0,1.0). 
    '''
    def __init__(self):
        super().__init__(parent=None, uv_rect=np.array([0.0,0.0,1.0,1.0]))
