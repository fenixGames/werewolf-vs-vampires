from typing import Callable

import pygame

from lib.events import Event
from lib.vector import Point
from src.board import MatchThreeBoard, Piece


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

        position = Point(event.pos[0], event.pos[1]) - offset - board.position

        prev_square = board.get_children_in_position(self.__previous)
        current_square = board.get_children_in_position(position)
        if prev_square is not None and prev_square.selected:
            if self.draw_function is not None:
                exchange_squares(prev_square, current_square, self.draw_function)

                board.swap_children(prev_square, current_square)
            board.reset_tiles()
            board.check_matches(prev_square, current_square)
        elif current_square is not None:
            current_square.selected = not current_square.selected
        self.__previous = position
