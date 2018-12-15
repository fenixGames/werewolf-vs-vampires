import sys
from typing import Tuple, List

import pygame

from src.game_object import GameObject


class Window:
    def __init__(self, width: int, height: int, title: str):
        self.__width: int = width
        self.__height: int = height
        self.__objects: List[GameObject] = []

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

    def draw_window(self):
        for obj in self.__objects:
            surface = obj.draw()
            if isinstance(surface, pygame.Surface):
                self.__screen.blit(surface, obj.position.to_tuple())
            elif isinstance(surface, pygame.Rect):
                pygame.draw.rect(self.__screen, obj.color, surface, 1)
        pygame.display.flip()

    @staticmethod
    def process_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
