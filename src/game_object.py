from typing import Tuple, Union

import pygame


class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def to_tuple(self) -> Tuple[int, int]:
        return self.x, self.y


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
        self.__outer_rect: Size = Size(size[0], size[1])
        self.__color: pygame.Color = None

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
    def outer_rect(self) -> Size:
        return self.__outer_rect

    @property
    def rectangle(self):
        return pygame.Rect(self.position.to_tuple(), self.outer_rect.to_tuple())

    def draw(self) -> Union[pygame.Surface, pygame.Rect]:
        pass
