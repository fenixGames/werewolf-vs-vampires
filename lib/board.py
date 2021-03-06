from typing import Tuple, List

import pygame

from lib.game_object import GameObject


class Board(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)

    def divide_board(self, square_width: int, square_height: int, colors: List[pygame.Color]):
        """ Divides a board equally using a tile width and height

        This is useful for boards like the chess one, for other boards, please generate the squares individually
        and append them to the list of squares of the class.

        :param square_width: the width of the squares
        :param square_height: the height of the squares
        :param colors: the list of colors used for the tiles, the colors are going to be rotated.
        """
        if self.size.width % square_width != 0:
            raise AttributeError(f'The board cannot be equally divided horizontally')
        if self.size.height % square_height != 0:
            raise AttributeError(f'The board cannot be equally divided vertically')

        square_size = square_width, square_height
        y_index = 0
        used_colors: List[pygame.Color] = []
        while y_index < self.size.height:
            x_index = 0
            while x_index < self.size.width:
                color = colors[0]
                square = Square((x_index, y_index), square_size)
                square.color = color

                used_colors.append(color)
                colors.remove(color)
                if not len(colors):
                    colors = used_colors
                    used_colors = []

                self.children.append(square)
                x_index += square_width
            y_index += square_height


class Square(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)
