from typing import List, Tuple

from lib.game_object import GameObject
from lib.vector import Point, Size
from src.piece import PieceType, Piece


class Column(GameObject):
    def __init__(self, position: Point, size: Size):
        super().__init__(position.to_tuple(), size.to_tuple())

    def reset_tiles(self):
        for child in self.children:
            child.selected = False

    def get_swaps_by_type(self, piece_type: PieceType):
        index = len(self.children) - 1
        swapped_pieces: List[Tuple[Piece, Piece]] = []
        while index > 0:
            piece = self.children[index]
            piece_above = self.children[index - 1]

            if piece.type == piece_type and piece_above.type != piece_type:
                swapped_pieces.append((piece, piece_above))
            index -= 1
        return swapped_pieces

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
