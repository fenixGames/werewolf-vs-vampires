import pathlib

import pygame

from lib.vector import Size, Point


class GraphicResource:
    def __init__(self, path_to_file: pathlib.Path, size: Size = None):
        if not path_to_file.absolute().is_file():
            raise FileNotFoundError(f'The image for the sprite {path_to_file.absolute().as_posix()} does not exist')

        self.__graphic: pygame.Surface = pygame.image.load(path_to_file.absolute().as_posix()).convert()

        if size is None:
            self.__size: Size = Size(self.__graphic.get_width(), self.__graphic.get_height())
        else:
            self.__size: Size = size
        self.__alpha_color: pygame.Color = (255, 255, 255, 255)

    @property
    def alpha_color(self) -> pygame.Color:
        return self.__alpha_color

    @alpha_color.setter
    def alpha_color(self, value: pygame.Color):
        self.__alpha_color = value

    @property
    def size(self) -> Size:
        return self.__size

    @property
    def drawable_surface(self) -> pygame.Surface:
        container: pygame.Surface = pygame.Surface(self.size.to_tuple())
        container.set_colorkey(self.alpha_color)
        container.fill(self.alpha_color)
        container.blit(self.__graphic, (0, 0))
        return container

    def overlap_resource(self, resource: __init__):
        self.__graphic.blit(resource.drawable_surface, (0, 0))


class Sprite:
    def __init__(self, sprite: GraphicResource, size: Size = None):
        self.__sprite: GraphicResource = sprite
        self.__alpha_color: pygame.Color = (255, 255, 255, 255)

        if size is None:
            self.__size = sprite.size
        else:
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

        x_offset = int((container.get_width() - self.__sprite.size.width) / 2)
        y_offset = int((container.get_height() - self.__sprite.size.width) / 2)

        position = Point(x_offset, y_offset) + offset
        container.blit(self.__sprite.drawable_surface, (x_offset, y_offset))

        surface.blit(container, position.to_tuple())
