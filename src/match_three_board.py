import pathlib
import random
from enum import Enum
from typing import Tuple, List

from src.game_object import GameObject, Point, Size


class MatchThreeBoard(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int], columns: int, rows: int):
        super().__init__(position, size)

        if columns < 0:
            raise AttributeError('The number of columns cannot be negative')
        if rows < 0:
            raise AttributeError('The number of rows cannot be negative')

        self.__columns: int = columns
        self.__rows: int = rows

    def init_board(self, tile_width: int, tile_height: int):
        offset = Point(int((self.size.width - tile_width * self.__columns) / 2),
                       int((self.size.height - tile_height * self.__rows) / 2))
        for row in range(0, self.__rows):
            for column in range(0, self.__columns):
                position = Point(row * tile_height, column * tile_width) + offset
                piece = GameObject(position.to_tuple(), (tile_width, tile_height))
                piece.sprite = Piece.as_list()[random.randrange(0, 6, 1)].value, Size(tile_width, tile_height)
                self.children.append(piece)


class Piece(Enum):
    YELLOW = pathlib.Path('resources/yellow.png')
    RED = pathlib.Path('resources/red.png')
    BLUE = pathlib.Path('resources/blue.png')
    PURPLE = pathlib.Path('resources/purple.png')
    GREEN = pathlib.Path('resources/green.png')
    BLACK = pathlib.Path('resources/black.png')

    @staticmethod
    def as_list() -> List:
        list_of_pieces = []
        for piece in Piece:
            list_of_pieces.append(piece)
        return list_of_pieces
