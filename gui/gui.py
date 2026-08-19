'''
The GUI system is basically a tree that resembles the folder/file system of operating systems.

There is a GUIManager class that holds the root node, which is the head of the tree. Various methods make possible
to build a GUI from code, through the GUIManager. You can add new containers or new GUI elements, whose configuration lives
in the apposit file.
'''

import pygame
from project.gui.gui_elems_config import *


class GUIManager:
    '''
    The main class used to build GUIs across the project. It holds a Root instance from which it operates along the tree structures
    '''
    def __init__(self):
        self.root = Root()
        self.current_container: Container = None

        self.set_current_container(self.root)


    def reset(self):
        self.root = Root()


    def set_current_container(self, container: Container):
        self.current_container = container


    def get_current_container(self):
        return self.current_container


    def back(self):
        parent = self.current_container.get_parent()
        self.set_current_container(parent)


    def add_container(self, uv_rect: tuple[float,float,float,float], color: pygame.Color = None):
        container = Container(parent=self.current_container, uv_rect=np.array(uv_rect))
        if color:
            container.set_color(color)
        self.current_container.add_child(child=container)
        self.set_current_container(container)


    def add_element(self, element: GUIElement):
        self.current_container.add_child(child=element)


    def update(self, dt):
        self.root.update(dt)


    def draw(self, surface: pygame.Surface):
        self.root.draw(surface)
