from typing import List, Dict, Union

from lib.game_object import GameObject
from lib.vector import Point, Size
from src.piece import PieceType, Piece


class Column(GameObject):
    def __init__(self, position: Point, size: Size):
        super().__init__(position.to_tuple(), size.to_tuple())
        self.__needs_filling: bool = False

    def reset_tiles(self):
        for child in self.children:
            child.selected = False

    def _get_first_occupied_square(self) -> Union[Piece, None]:
        idx = len(self.children) - 1
        while idx >= 0:
            child: Piece = self.children[idx]
            if child.type != PieceType.EMPTY:
                return child
            idx -= 1
        return None

    def _get_first_unoccupied_square(self) -> Union[Piece, None]:
        idx = len(self.children) - 1
        while idx >= 0:
            piece: Piece = self.children[idx]
            if piece.type == PieceType.EMPTY:
                return piece
            idx -= 1
        return None

    def get_dropping_squares(self) -> Dict[Piece, Point]:
        dropping_pieces: Dict[Piece, Point] = {}

        occupied = self._get_first_occupied_square()
        empty = self._get_first_unoccupied_square()

        if empty is None:
            return {}
        if occupied is None:
            self.fill_column(len(self.children))
            new_items: int = len(self.children)
        else:
            index_occupied = self.children.index(occupied)
            index_empty = self.children.index(empty)

            if index_occupied > index_empty:
                self.fill_column(index_empty + 1)
                new_items = index_empty + 1
            else:
                point = Point(empty.position.x, empty.position.y)
                delta_point = Point(0, Piece.PIECE_SIZE.height)
                idx = index_occupied
                while idx >= 0:
                    dropping_pieces[self.children[idx]] = point
                    point = point - delta_point
                    idx -= 1
                self.fill_column(index_empty + 1, index_occupied + 1)
                new_items = index_empty - index_occupied + 1
        for idx in range(0, new_items):
            piece = self.children[idx]
            dropping_pieces[piece] = Point(0, idx * Piece.PIECE_SIZE.height)

        return dropping_pieces

    def get_matches(self, piece: Piece, row: int) -> List[Piece]:
        matches: List[Piece] = []

        # Check upwards
        index = row - 1
        while index >= 0 and self.children[index].type == piece.type:
            matches.append(self.children[index])
            index -= 1

        # Check downwards
        index = row + 1
        while index < len(self.children) and self.children[index].type == piece.type:
            matches.append(self.children[index])
            index += 1

        if len(matches) > 1:
            matches.append(piece)
            return matches
        return []

    def fill_column(self) -> List[Piece]:
        if not self.__needs_filling:
            return []

        for index in range(0, column_length):
            self._new_piece()

    @staticmethod
    def _new_piece() -> Piece:
        piece = Piece((0, 0), Piece.PIECE_SIZE.to_tuple())
        piece.type = PieceType.get_random_piece()
        return piece

    def fill_column(self, amount: int, offset: int = 0):
        for idx in range(offset, amount):
            piece = self._new_piece()
            self.children.remove(self.children[idx])
            self.children.insert(0, piece)
