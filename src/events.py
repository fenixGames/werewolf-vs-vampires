import time
from typing import Tuple, List, Callable

import pygame

from lib import movement
from lib.events import Event
from lib.movement import MovementAnimation
from lib.vector import Point
from src.board import MatchThreeBoard
from src.piece import Piece, PieceType


def animate_swap(piece1: Piece,
                 piece2: Piece,
                 draw_function: Callable[[], None],
                 board: MatchThreeBoard) -> List[MovementAnimation]:
    animations: List[MovementAnimation] = []

    row1, column1 = board.get_position_of_piece(piece1)
    row2, column2 = board.get_position_of_piece(piece2)

    final_position1 = Point(piece2.position.x, piece2.position.y)
    final_position2 = Point(piece1.position.x, piece1.position.y)
    if column1 < column2:
        final_position1.x += piece1.size.width
        final_position2.x -= piece1.size.width
    elif column1 > column2:
        final_position1.x -= piece1.size.width
        final_position2.x += piece1.size.width

    animation1 = MovementAnimation(draw_function, piece1, movement.linear_movement, final_position1)
    animation2 = MovementAnimation(draw_function, piece2, movement.linear_movement, final_position2)

    animation1.start()
    animation2.start()

    animations.append(animation1)
    animations.append(animation2)
    return animations


class MouseButtonDownEvent(Event):
    def __init__(self, board: MatchThreeBoard, offset: Point):
        super().__init__(pygame.MOUSEBUTTONDOWN, (board, offset))
        self.__previous: Point = Point(0, 0)

    def handle(self, event: pygame.event.Event):
        board: MatchThreeBoard = None
        offset: int = -1

        animations: List[MovementAnimation] = []
        if event.button != 1:
            return
        board, offset = self.args

        position = Point(event.pos[0], event.pos[1]) - offset

        prev_square = board.get_children_in_position(self.__previous)
        current_square = board.get_children_in_position(position)

        if current_square is None:
            return
        if not board.are_neighbours(prev_square, current_square):
            board.reset_tiles()
            current_square.selected = True
        elif prev_square is not None and current_square is not None and prev_square == current_square:
            current_square.selected = not current_square.selected
        elif prev_square is not None and prev_square.selected:
            if self.draw_function is not None:
                animations += animate_swap(prev_square, current_square, self.draw_function, board)

            for animation in animations:
                animation.join()

            animations.clear()
            board.swap_children(prev_square, current_square)
            board.reset_tiles()
            self.handle_matches((prev_square, current_square), board)
        self.__previous = position

    def handle_matches(self, pieces: Tuple[Piece, Piece], board: MatchThreeBoard):
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
            animations: List[MovementAnimation] = []
            while swapped_pieces:
                for piece1, piece2 in swapped_pieces:
                    animations += animate_swap(piece1, piece2, self.draw_function, board)

                for animation in animations:
                    animation.join()
                animations.clear()

                for piece1, piece2 in swapped_pieces:
                    board.swap_children(piece1, piece2)
                swapped_pieces = board.get_swaps_by_type(PieceType.EMPTY)

            # for piece1, piece2 in swapped_pieces:
            #     self.handle_matches((piece1, piece2))
