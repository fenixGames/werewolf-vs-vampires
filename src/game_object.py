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


class GameObject:
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        self.__position: Point = Point(position[0], position[1])
        self.__size: Size = Size(size[0], size[1])
        self.__color: pygame.Color = None
        self.__children: List[GameObject] = []
        self.__only_border: bool = False
        self.__sprite: pygame.Surface = None

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
    def sprite(self) -> pygame.Surface:
        return self.__sprite

    @sprite.setter
    def sprite(self, path_to_sprite: pathlib.Path):
        if not path_to_sprite.absolute().is_file():
            raise FileNotFoundError(f'Sprite {path_to_sprite.absolute().as_posix()} not found')
        sprite: pygame.Surface = pygame.image.load(path_to_sprite.absolute().as_posix()).convert()
        self.__sprite: pygame.Surface = pygame.Surface(self.size.to_tuple())
        self.__sprite.set_colorkey((255, 255, 255, 255))
        self.__sprite.blit(sprite, (0, 0))

    def draw(self, surface: pygame.Surface, offset: Point):
        border = 1 if self.only_border else 0

        absolute_position = self.position + offset
        if self.sprite is not None:
            surface.blit(self.sprite, absolute_position.to_tuple())
        elif self.color is not None:
            pygame.draw.rect(surface, self.color, pygame.Rect(absolute_position.to_tuple(), self.size.to_tuple()),
                             border)

        for child in self.children:
            child.draw(surface, absolute_position)
