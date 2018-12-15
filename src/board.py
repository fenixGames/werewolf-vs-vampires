import pathlib
from typing import Tuple

import pygame

from src.game_object import GameObject


class Board(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)
        self.__background: pygame.Surface = None
        self.__color: Tuple[int, int, int] = None

    @property
    def background(self) -> pygame.Surface:
        return self.__background

    @background.setter
    def background(self, path_to_image: pathlib.Path):
        if not path_to_image.absolute().is_file():
            raise FileNotFoundError(f'The image for the board {path_to_image.absolute().as_uri()} does not exist')
        self.__background = pygame.image.load(path_to_image.absolute().as_posix()).convert()

    @property
    def color(self) -> Tuple[int, int, int]:
        return self.__color

    @color.setter
    def color(self, rgb: Tuple[int, int, int]):
        red, green, blue = rgb
        if red < 0 or red > 255:
            raise AttributeError(f'Invalid RGB color ({red}, {green}, {blue})')
        if green < 0 or green > 255:
            raise AttributeError(f'Invalid RGB color ({red}, {green}, {blue})')
        if blue < 0 or blue > 255:
            raise AttributeError(f'Invalid RGB color ({red}, {green}, {blue})')
        self.__color = red, green, blue

    def draw(self) -> pygame.Surface:
        if self.background is not None:
            return self.background
        if self.color is not None:
            board: pygame.Surface = pygame.Surface(self.outer_rect.to_tuple())
            board.fill(self.color, pygame.Rect(self.position.x, self.position.y, self.outer_rect.width - 1,
                                               self.outer_rect.height - 1))
            return board
