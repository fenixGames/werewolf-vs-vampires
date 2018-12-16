import sys
from typing import Tuple, List

import pygame

from src.game_object import GameObject
from src.vector import Point


class Window:
    def __init__(self, width: int, height: int, title: str):
        self.__width: int = width
        self.__height: int = height
        self.__objects: List[GameObject] = []
        self.__color: pygame.Color = None

        pygame.init()
        self.__screen: pygame.Surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(title)

    @property
    def width(self) -> int:
        return self.__width

    @property
    def height(self) -> int:
        return self.__height

    @property
    def size(self) -> Tuple[int, int]:
        return self.width, self.height

    @property
    def objects(self) -> List[GameObject]:
        return self.__objects

    @property
    def color(self) -> pygame.Color:
        return self.__color

    @color.setter
    def color(self, rgb: pygame.Color):
        self.__color = rgb

    def draw_window(self):
        if self.color is not None:
            self.__screen.fill(self.color)

        for obj in self.__objects:
            obj.draw(self.__screen, Point(0, 0))
        pygame.display.flip()

    @staticmethod
    def process_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
