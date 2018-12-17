import time
from typing import Callable, Tuple

import pygame

from lib.events import Event
from lib.vector import Point
from src.board import MatchThreeBoard
from src.piece import Piece, PieceType


def exchange_squares(chosen_square: Piece, selected_square: Piece, draw_function: Callable):
    delta_point: Point = chosen_square.position - selected_square.position
    delta_point.x /= 10
    delta_point.y /= 10

    final_position = selected_square.position
    while chosen_square.position != final_position:
        chosen_square.position -= delta_point
        selected_square.position += delta_point

        draw_function()


class MouseButtonDownEvent(Event):
    def __init__(self, board: MatchThreeBoard, offset: Point):
        super().__init__(pygame.MOUSEBUTTONDOWN, (board, offset))
        self.__previous: Point = Point(0, 0)

    def handle(self, event: pygame.event.Event):
        board: MatchThreeBoard = None
        offset: int = -1
        if event.button != 1:
            return
        board, offset = self.args

        position = Point(event.pos[0], event.pos[1]) - offset

        prev_square = board.get_children_in_position(self.__previous)
        current_square = board.get_children_in_position(position)

        if not board.are_neighbours(prev_square, current_square):
            board.reset_tiles()
            current_square.selected = True
        elif prev_square is not None and current_square is not None and prev_square == current_square:
            current_square.selected = not current_square.selected
        elif prev_square is not None and prev_square.selected:
            if self.draw_function is not None:
                exchange_squares(prev_square, current_square, self.draw_function)

                board.swap_children(prev_square, current_square)
            board.reset_tiles()
            self.handle_matches((prev_square, current_square))
            pass
        self.__previous = position

    def handle_matches(self, pieces: Tuple[Piece, Piece]):
        board: MatchThreeBoard = None
        board, _ = self.args

        for piece in pieces:
            matches = board.get_match_list(piece)

            for match in matches:
                match.selected = True
            self.draw_function()

            time.sleep(0.2)
            for match in matches:
                match.type = PieceType.EMPTY
                match.selected = False
            self.draw_function()

            swapped_pieces = board.get_swaps_by_type(PieceType.EMPTY)
            while swapped_pieces:
                for piece1, piece2 in swapped_pieces:
                    exchange_squares(piece1, piece2, self.draw_function)
                    board.swap_children(piece1, piece2)
                swapped_pieces = board.get_swaps_by_type(PieceType.EMPTY)

            # for piece1, piece2 in swapped_pieces:
            #     self.handle_matches((piece1, piece2))
