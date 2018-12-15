import pathlib
from typing import Tuple, Union, List

import pygame

from src.game_object import GameObject


class Board(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)
        self.__background: pygame.Surface = None
        self.__square_list: List[Square] = []

    @property
    def background(self) -> pygame.Surface:
        return self.__background

    @background.setter
    def background(self, path_to_image: pathlib.Path):
        if not path_to_image.absolute().is_file():
            raise FileNotFoundError(f'The image for the board {path_to_image.absolute().as_uri()} does not exist')
        self.__background = pygame.image.load(path_to_image.absolute().as_posix()).convert()

    @property
    def square_list(self):
        return self.__square_list

    def divide_board(self, square_width: int, square_height: int, colors: List[pygame.Color]):
        """ Divides a board equally using a tile width and height

        This is useful for boards like the chess one, for other boards, please generate the squares individually
        and append them to the list of squares of the class.

        :param square_width: the width of the squares
        :param square_height: the height of the squares
        :param colors: the list of colors used for the tiles, the colors are going to be rotated.
        """
        if self.outer_rect.width % square_width != 0:
            raise AttributeError(f'The board cannot be equally divided horizontally')
        if self.outer_rect.height % square_height != 0:
            raise AttributeError(f'The board cannot be equally divided vertically')

        square_size = square_width, square_height
        y_index = 0
        used_colors: List[pygame.Color] = []
        while y_index < self.outer_rect.height:
            x_index = 0
            while x_index < self.outer_rect.width:
                color = colors[0]
                square = Square((x_index, y_index), square_size)
                square.color = color

                used_colors.append(color)
                colors.remove(color)
                if not len(colors):
                    colors = used_colors
                    used_colors = []

                self.square_list.append(square)
                x_index += square_width
            y_index += square_height

    def draw(self) -> Union[pygame.Surface, pygame.Rect]:
        board_surface: pygame.Surface = pygame.Surface(self.outer_rect.to_tuple())
        if self.background is not None:
            board_surface.blit(self.background, self.position.to_tuple())
        if self.color is not None:
            pygame.draw.rect(board_surface, self.color, self.rectangle, 1)

        for square in self.square_list:
            surface = square.draw()
            if isinstance(surface, pygame.Rect):
                pygame.draw.rect(board_surface, square.color, surface)
            elif isinstance(surface, pygame.Surface):
                board_surface.blit(surface, square.position.to_tuple())
        return board_surface


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
