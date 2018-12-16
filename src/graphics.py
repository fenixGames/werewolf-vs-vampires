import pathlib

import pygame

from src.vector import Size, Point


class Sprite:
    def __init__(self, path_to_file: pathlib.Path, size: Size):
        if not path_to_file.absolute().is_file():
            raise FileNotFoundError(f'The file for the sprite {path_to_file.absolute().as_posix()} does not exist')

        self.__sprite: pygame.Surface = pygame.image.load(path_to_file.absolute().as_posix()).convert()
        self.__alpha_color: pygame.Color = (255, 255, 255, 255)
        self.__size: Size = size

    @property
    def alpha_color(self) -> pygame.Color:
        return self.__alpha_color

    @alpha_color.setter
    def alpha_color(self, value: pygame.Color):
        self.__alpha_color = value

    def draw(self, surface: pygame.Surface, offset: Point):
        container = pygame.Surface(self.__size.to_tuple())
        container.set_colorkey(self.__alpha_color)
        container.fill(self.__alpha_color)

        x_offset = int((container.get_width() - self.__sprite.get_width()) / 2)
        y_offset = int((container.get_height() - self.__sprite.get_height()) / 2)

        position = Point(x_offset, y_offset) + offset
        container.blit(self.__sprite, (x_offset, y_offset))

        surface.blit(container, position.to_tuple())