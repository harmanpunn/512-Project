"""
Class that handles all the rendering part of the project

"""
import pygame
from environment import Environment
from graph import Graph


class Renderer:
    """
    Initializes the screen 
    Parameters:
        graph -> generated graph object 
    """
    def __init__(self, graph : Graph) -> None:
        if Environment.getInstance().ui:
            pygame.init()
            self.surface = pygame.display.set_mode((500, 500))
            pygame.display.set_caption('Circle of Life')
    

    # Rendering
    def __render__(self):
        pass