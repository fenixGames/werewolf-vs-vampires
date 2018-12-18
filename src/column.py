from typing import List

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

    def get_dropping_squares(self, piece_type: PieceType) -> List[Piece]:
        index = len(self.children) - 1
        swapped_pieces: List[Piece] = []
        while index >= 0:
            piece = self.children[index]

            if piece.type == piece_type:
                self.children.remove(piece)
                self.__needs_filling = True
                idx = index - 1
                while idx >= 0:
                    swapped_pieces.append(self.children[idx])
                    idx -= 1
                return swapped_pieces
            index -= 1
        return []

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

        self.__needs_filling = False
        piece = Piece((0, 0), self.children[0].size.to_tuple())
        piece.type = PieceType.get_random_piece()

        self.children.insert(0, piece)

        return [piece]
