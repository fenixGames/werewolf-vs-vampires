import pathlib
import random
from enum import Enum
from typing import Tuple, List

from lib.game_object import GameObject
from lib.graphics import GraphicResource
from lib.vector import Size


class PieceType(Enum):
    YELLOW = pathlib.Path('resources/yellow.png')
    RED = pathlib.Path('resources/red.png')
    BLUE = pathlib.Path('resources/blue.png')
    PURPLE = pathlib.Path('resources/purple.png')
    GREEN = pathlib.Path('resources/green.png')
    BLACK = pathlib.Path('resources/black.png')
    EMPTY = pathlib.Path('resources/empty.png')

    @staticmethod
    def as_list() -> List:
        list_of_pieces = []
        for piece in PieceType:
            list_of_pieces.append(piece)
        return list_of_pieces

    @staticmethod
    def get_random_piece():
        return PieceType.as_list()[random.randrange(0, 6, 1)]


def is_column_combination(board: List[List[PieceType]], column: int, row: int, new_piece: PieceType) -> bool:
    if column < 2:
        return False
    elif board[row][column - 1] == new_piece and board[row][column - 2] == new_piece:
        return True
    return False


def is_row_combination(board: List[List[PieceType]], column: int, row: int, new_piece: Enum) -> bool:
    if row < 2:
        return False
    elif board[row - 1][column] == new_piece and board[row - 2][column] == new_piece:
        return True
    return False


class Piece(GameObject):
    PIECE_SIZE: Size = Size(0, 0)

    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)
        self.__selected: bool = False
        self.__type: PieceType = None
        self.PIECE_SIZE.width = size[0]
        self.PIECE_SIZE.height = size[1]

    @property
    def selected(self) -> bool:
        return self.__selected

    @selected.setter
    def selected(self, value: bool):
        self.__selected = value

        self.reload_sprite()

    def reload_sprite(self):
        if not self.selected:
            self.sprite = GraphicResource(self.type.value)
        else:
            sprite = GraphicResource(self.type.value)
            sprite.overlap_resource(GraphicResource(pathlib.Path('resources/selection.png')))
            self.sprite = sprite

    @property
    def type(self) -> PieceType:
        return self.__type

    @type.setter
    def type(self, value: PieceType):
        self.__type = value
        self.reload_sprite()

    # def __eq__(self, other) -> bool:
    #     if not isinstance(other, Piece):
    #         return False
    #     return self.position == other.position
