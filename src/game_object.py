import pathlib
from typing import Tuple, List

import pygame


class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)


class Size:
    def __init__(self, width: int, height: int):
        if width < 0:
            raise AttributeError("The width of an object cannot be negative")
        if height < 0:
            raise AttributeError("The height of the object cannot be negative")
        self.width: int = width
        self.height: int = height

    def to_tuple(self) -> Tuple[int, int]:
        return self.width, self.height


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


class GameObject:
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        self.__position: Point = Point(position[0], position[1])
        self.__size: Size = Size(size[0], size[1])
        self.__color: pygame.Color = None
        self.__children: List[GameObject] = []
        self.__only_border: bool = False
        self.__sprite: Sprite = None

    @property
    def color(self) -> pygame.Color:
        return self.__color

    @color.setter
    def color(self, color: pygame.Color):
        self.__color = color

    @property
    def position(self) -> Point:
        return self.__position

    @property
    def size(self) -> Size:
        return self.__size

    @property
    def children(self):
        return self.__children

    @property
    def rectangle(self):
        return pygame.Rect(self.position.to_tuple(), self.size.to_tuple())

    @property
    def only_border(self) -> bool:
        return self.__only_border

    @only_border.setter
    def only_border(self, value: bool):
        if not isinstance(value, bool):
            raise AttributeError(f'Value is not boolean, {value} ({type(value)})')
        self.__only_border = value

    @property
    def sprite(self) -> Sprite:
        return self.__sprite

    @sprite.setter
    def sprite(self, value: Tuple[pathlib.Path, Size]):
        self.__sprite = Sprite(value[0], value[1])

    def draw(self, surface: pygame.Surface, offset: Point):
        border = 1 if self.only_border else 0

        absolute_position = self.position + offset
        if self.sprite is not None:
            self.sprite.draw(surface, absolute_position)
        elif self.color is not None:
            pygame.draw.rect(surface, self.color, pygame.Rect(absolute_position.to_tuple(), self.size.to_tuple()),
                             border)

        for child in self.children:
            child.draw(surface, absolute_position)
