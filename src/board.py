from typing import Tuple, List

import src
from lib.game_object import GameObject
from lib.graphics import GraphicResource
from lib.vector import Point, Size
from src.column import Column
from src.piece import Piece, PieceType


class MatchThreeBoard(GameObject):
    def __init__(self, position: Tuple[int, int], size: Tuple[int, int]):
        super().__init__(position, size)

    def get_match_list(self, piece: Piece) -> List[Piece]:
        if piece.type == PieceType.EMPTY:
            return []
        row, column = self.get_position_of_piece(piece)
        column_matches = self.children[column].get_matches(piece=piece, row=row)
        row_matches = self.get_matches_on_row(piece=piece, row=row, column=column)

        return column_matches + row_matches

    def reset_tiles(self):
        for child in self.children:
            child.reset_tiles()

    def swap_children(self, swap1: Piece, swap2: Piece):
        row1, column1 = self.get_position_of_piece(swap1)
        row2, column2 = self.get_position_of_piece(swap2)

        self.children[column1].children[row1], self.children[column2].children[row2] = \
            self.children[column2].children[row2], self.children[column1].children[row1]

        if column1 != column2:
            self.children[column1].children[row1].position.x = 0
            self.children[column2].children[row2].position.x = 0
        return None

    def get_matches_on_row(self, piece: Piece, row: int, column: int) -> List[Piece]:
        piece_type: PieceType = piece.type
        row_matches: List[Piece] = []

        # Check left
        idx = column - 1
        while idx >= 0 and self.children[idx].children[row].type == piece_type:
            row_matches.append(self.children[idx].children[row])
            idx -= 1

        # CHeck right
        idx = column + 1
        while idx < len(self.children) and self.children[idx].children[row].type == piece_type:
            row_matches.append(self.children[idx].children[row])
            idx += 1

        if len(row_matches) > 1:
            row_matches.append(piece)
            return row_matches
        return []

    def get_position_of_piece(self, piece: Piece) -> Tuple[int, int]:
        row, column = -1, -1
        for child in self.children:
            if piece in child.children:
                column = self.children.index(child)
                row = child.children.index(piece)
                break
        return row, column

    def fill_board(self) -> List[Piece]:
        new_swaps: List[Piece] = []
        for column in self.children:
            new_swaps += column.fill_column()
        return new_swaps

    def get_swaps_by_type(self, piece_type: PieceType):
        new_swaps: List[Tuple[Piece, Piece]] = []
        for column in range(0, len(self.children)):
            new_swaps += self.children[column].get_swaps_by_type(piece_type)
        return new_swaps

    def are_neighbours(self, piece1: Piece, piece2: Piece) -> bool:
        row1, column1 = self.get_position_of_piece(piece1)
        row2, column2 = self.get_position_of_piece(piece2)

        if row1 == row2 and column2 == column1:
            return True

        # Check same row
        if row1 == row2 and (column1 == column2 - 1 or column1 == column2 + 1):
            return True

        if column1 == column2 and (row1 == row2 - 1 or row1 == row2 + 1):
            return True
        return False


def create_board(position: Point, size: Size, columns: int, rows: int, tile_size: Size) -> MatchThreeBoard:
    if columns < 0:
        raise AttributeError(f'The number of columns must be positive')
    if rows < 0:
        raise AttributeError(f'The number of rows must be positive')

    offset = Point(int((size.width - tile_size.width * columns) / 2),
                   int((size.height - tile_size.height * rows) / 2))
    board = MatchThreeBoard(position.to_tuple(), size.to_tuple())

    type_board: List[List[PieceType]] = []
    for index in range(0, columns):
        position = Point(index * tile_size.height, 0) + offset
        column = Column(position, Size(tile_size.width, tile_size.height * rows))
        for row in range(0, rows):
            if len(type_board) <= row:
                type_board.append([])
            position = Point(0, row * tile_size.width)
            piece = Piece(position.to_tuple(), tile_size.to_tuple())

            is_match = True
            new_piece = PieceType.BLACK
            while is_match:
                new_piece = PieceType.get_random_piece()
                is_match = src.piece.is_column_combination(board=type_board, column=index, row=row, new_piece=new_piece)
                is_match = is_match or src.piece.is_row_combination(board=type_board, column=index, row=row,
                                                                    new_piece=new_piece)
            piece.sprite = GraphicResource(new_piece.value, tile_size)
            piece.type = new_piece
            type_board[row].append(new_piece)
            column.children.append(piece)

        board.children.append(column)
    return board
