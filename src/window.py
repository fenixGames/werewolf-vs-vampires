import sys
from typing import Tuple

import pygame


class Window:
    def __init__(self, width: int, height: int, title: str):
        self.__width: int = width
        self.__height: int = height

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

    @staticmethod
    def draw_window():
        pygame.display.flip()

    @staticmethod
    def process_events():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
