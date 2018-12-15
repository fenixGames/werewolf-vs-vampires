import pathlib
from typing import Tuple, Union

import pygame

from src.game_object import GameObject


class Board(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)
        self.__background: pygame.Surface = None

    @property
    def background(self) -> pygame.Surface:
        return self.__background

    @background.setter
    def background(self, path_to_image: pathlib.Path):
        if not path_to_image.absolute().is_file():
            raise FileNotFoundError(f'The image for the board {path_to_image.absolute().as_uri()} does not exist')
        self.__background = pygame.image.load(path_to_image.absolute().as_posix()).convert()

    def draw(self) -> Union[pygame.Surface, pygame.Rect]:
        if self.background is not None:
            return self.background
        if self.color is not None:
            return self.rectangle


class Square(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)
        self.__sprite: pygame.Surface = None

    @property
    def sprite(self) -> pygame.Surface:
        return self.__sprite

    @sprite.setter
    def sprite(self, path_to_file: pathlib.Path):
        if not path_to_file.absolute().is_file():
            raise FileNotFoundError(f'The sprite for the square {path_to_file.absolute().as_uri()} does not exist')
        self.__sprite = pygame.image.load(path_to_file.absolute().as_posix()).convert()

    def draw(self):
        if self.sprite is not None:
            return self.sprite
        if self.color is not None:
            return self.rectangle
