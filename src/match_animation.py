import time
from typing import Callable

from lib.animation import Animation
from src.piece import Piece, PieceType


class MatchAnimation(Animation):
    def __init__(self, draw_function: Callable[[], None], piece: Piece):
        super().__init__(draw_function)
        self.__piece: Piece = piece

    def run(self):
        self.__piece.selected = True
        self.draw_screen()
        time.sleep(0.5)
        self.__piece.selected = False
        self.__piece.type = PieceType.EMPTY
        self.draw_screen()
