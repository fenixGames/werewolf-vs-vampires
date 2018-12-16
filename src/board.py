import pathlib
import random
from enum import Enum
from typing import Tuple, List

from lib.game_object import GameObject
from lib.graphics import GraphicResource
from lib.vector import Point, Size


class PieceType(Enum):
    YELLOW = pathlib.Path('resources/yellow.png')
    RED = pathlib.Path('resources/red.png')
    BLUE = pathlib.Path('resources/blue.png')
    PURPLE = pathlib.Path('resources/purple.png')
    GREEN = pathlib.Path('resources/green.png')
    BLACK = pathlib.Path('resources/black.png')

    @staticmethod
    def as_list() -> List:
        list_of_pieces = []
        for piece in PieceType:
            list_of_pieces.append(piece)
        return list_of_pieces


class Piece(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)
        self.__selected: bool = False
        self.__type: PieceType = None

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


class MatchThreeBoard(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int], columns: int, rows: int):
        super().__init__(position, size)

        if columns < 0:
            raise AttributeError('The number of columns cannot be negative')
        if rows < 0:
            raise AttributeError('The number of rows cannot be negative')

        self.__columns: int = columns
        self.__rows: int = rows
        self.__board: List[List[PieceType]] = []

    def init_board(self, tile_width: int, tile_height: int):
        offset = Point(int((self.size.width - tile_width * self.__columns) / 2),
                       int((self.size.height - tile_height * self.__rows) / 2))
        for row in range(0, self.__rows):
            self.__board.append([])
            for column in range(0, self.__columns):
                position = Point(row * tile_height, column * tile_width) + offset
                piece = Piece(position.to_tuple(), (tile_width, tile_height))

                is_match = True
                new_piece = PieceType.BLACK
                while is_match:
                    new_piece = PieceType.as_list()[random.randrange(0, 6, 1)]
                    is_match = self.is_column_combination(column=column, row=row, new_piece=new_piece)
                    is_match = is_match or self.is_row_combination(column=column, row=row, new_piece=new_piece)

                piece.sprite = GraphicResource(new_piece.value, Size(tile_width, tile_height))
                piece.type = new_piece
                self.__board[row].append(new_piece)
                self.children.append(piece)

    def is_column_combination(self, column, new_piece, row):
        if column < 2:
            return False
        elif self.__board[row][column - 1] == new_piece and self.__board[row][column - 2] == new_piece:
            return True
        return False

    def is_row_combination(self, column: int, row: int, new_piece: Enum) -> bool:
        if row < 2:
            return False
        elif self.__board[row - 1][column] == new_piece and self.__board[row - 2][column] == new_piece:
            return True
        return False

    def child_in_position(self, position: Point) -> Union[GameObject, None]:
        for child in self.children:
            if child.position == position:
                return child
        return None


class PieceType(Enum):
    YELLOW = pathlib.Path('resources/yellow.png')
    RED = pathlib.Path('resources/red.png')
    BLUE = pathlib.Path('resources/blue.png')
    PURPLE = pathlib.Path('resources/purple.png')
    GREEN = pathlib.Path('resources/green.png')
    BLACK = pathlib.Path('resources/black.png')

    @staticmethod
    def as_list() -> List:
        list_of_pieces = []
        for piece in PieceType:
            list_of_pieces.append(piece)
        return list_of_pieces
