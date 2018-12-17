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
    EMPTY = pathlib.Path('resources/empty.png')

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

    def init_board(self, tile_width: int, tile_height: int):
        offset = Point(int((self.size.width - tile_width * self.__columns) / 2),
                       int((self.size.height - tile_height * self.__rows) / 2))
        board: List[List[PieceType]] = []
        for row in range(0, self.__rows):
            board.append([])
            for column in range(0, self.__columns):
                position = Point(column * tile_height, row * tile_width) + offset
                piece = Piece(position.to_tuple(), (tile_width, tile_height))

                is_match = True
                new_piece = PieceType.BLACK
                while is_match:
                    new_piece = PieceType.as_list()[random.randrange(0, 6, 1)]
                    is_match = self.is_column_combination(board=board, column=column, row=row, new_piece=new_piece)
                    is_match = is_match or self.is_row_combination(board=board, column=column, row=row,
                                                                   new_piece=new_piece)

                piece.sprite = GraphicResource(new_piece.value, Size(tile_width, tile_height))
                piece.type = new_piece
                board[row].append(new_piece)
                self.children.append(piece)

    def check_matches(self, swap1: Piece, swap2: Piece) -> bool:
        x_delta = self.children[0].size.width
        y_delta = self.children[0].size.height
        match_list: List[Piece] = []

        column_matches = self.get_matches_on_column(swap1)
        column_matches += self.get_matches_on_column(swap2)
        return True

    @staticmethod
    def is_column_combination(board: List[List[PieceType]], column: int, row: int, new_piece: PieceType) -> bool:
        if column < 2:
            return False
        elif board[row][column - 1] == new_piece and board[row][column - 2] == new_piece:
            return True
        return False

    @staticmethod
    def is_row_combination(board: List[List[PieceType]], column: int, row: int, new_piece: Enum) -> bool:
        if row < 2:
            return False
        elif board[row - 1][column] == new_piece and board[row - 2][column] == new_piece:
            return True
        return False

    def reset_tiles(self):
        for child in self.children:
            child.selected = False

    def get_children_in_position(self, position: Point) -> Piece:
        for child in self.children:
            if child.in_position(position):
                return child

    def get_matches_on_column(self, piece: Piece) -> List[Piece]:
        index: int = self.children.index(piece)
        piece_type: PieceType = self.children[index].type

        active_column = int(index % self.__columns)

        column_matches: List[Piece] = []

        # Check up
        idx = index - self.__columns
        while idx % self.__columns == active_column and idx >= 0 and self.children[idx].type == piece_type:
            column_matches.append(self.children[idx])
            idx -= self.__columns

        # Check down
        idx = index + self.__columns
        while idx % self.__columns == active_column and idx <= len(self.children) and \
                self.children[idx].type == piece_type:
            column_matches.append(self.children[idx])
            idx += self.__columns

        if len(column_matches) > 1:
            column_matches.append(piece)
            return column_matches
        return []

    def swap_children(self, swap1: Piece, swap2: Piece):
        idx1 = self.children.index(swap1)
        idx2 = self.children.index(swap2)

        self.children[idx1], self.children[idx2] = self.children[idx2], self.children[idx1]
        return None
