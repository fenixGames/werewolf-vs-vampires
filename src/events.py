import pygame

from lib.events import Event
from lib.vector import Point, Size
from src.board import MatchThreeBoard, Piece


class MouseButtonDownEvent(Event):
    def __init__(self, board: MatchThreeBoard, offset: Point):
        super().__init__(pygame.MOUSEBUTTONDOWN, (board, offset))

    def handle(self, event: pygame.event.Event):
        board, offset = self.args

        tile_size: Size = board.children[0].size

        position = Point(event.pos[0], event.pos[1]) - offset - board.position
        upper_position = position - Point(0, tile_size.height)
        bottom_position = position + Point(0, tile_size.height)
        left_position = position - Point(tile_size.width, 0)
        right_position = position + Point(tile_size.width, 0)

        selected_square: Piece = None
        chosen_square: Piece = None
        for square in board.children:
            if square.in_position(upper_position) and square.selected:
                selected_square = square
            if square.in_position(bottom_position) and square.selected:
                selected_square = square
            if square.in_position(left_position) and square.selected:
                selected_square = square
            if square.in_position(right_position) and square.selected:
                selected_square = square
            if square.in_position(position):
                chosen_square = square

        if selected_square is not None:
            chosen_square_type = chosen_square.type
            chosen_square.type = selected_square.type
            selected_square.type = chosen_square_type
            selected_square.selected = False
        elif chosen_square is not None:
            chosen_square.selected = not chosen_square.selected
