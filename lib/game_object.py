from typing import Tuple, List, Union

import pygame

from lib.graphics import Sprite, GraphicResource
from lib.vector import Point, Size


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

    @position.setter
    def position(self, value: Point):
        self.__position = value

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
    def sprite(self, value: Union[Tuple[GraphicResource, Size], GraphicResource]):
        if isinstance(value, GraphicResource):
            self.__sprite = Sprite(value)
        else:
            self.__sprite = Sprite(value[0], value[1])

    def in_position(self, position: Point):
        if position.x < self.position.x:
            return False
        if position.x > self.position.x + self.size.width:
            return False
        if position.y < self.position.y:
            return False
        if position.y > self.position.y + self.size.height:
            return False
        return True

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
