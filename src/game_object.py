from typing import Tuple


class Point:
    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y


class Size:
    def __init__(self, width: int, height: int):
        if width < 0:
            raise AttributeError("The width of an object cannot be negative")
        if height < 0:
            raise AttributeError("The height of the object cannot be negative")
        self.width: int = width
        self.height: int = height


class GameObject:
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        self.__position: Point = position
        self.__outer_rect: Size = Size(size[0], size[1])

    @property
    def position(self) -> Point:
        return self.__position

    @property
    def outer_rect(self) -> Size:
        return self.__outer_rect

    def draw(self):
        pass
