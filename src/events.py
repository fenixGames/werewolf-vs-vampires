from typing import List, Callable, Dict

import pygame

from lib import movement
from lib.events import Event
from lib.movement import MovementAnimation
from lib.vector import Point
from src.board import MatchThreeBoard
from src.match_animation import MatchAnimation
from src.piece import Piece


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
        step_point = Point(- Piece.PIECE_SIZE.width / 10, 0)
    elif column1 > column2:
        final_position1.x -= piece1.size.width
        final_position2.x += piece1.size.width
        step_point = Point(Piece.PIECE_SIZE.width / 10, 0)
    elif row1 < row2:
        step_point = Point(0, - Piece.PIECE_SIZE.height / 10)
    else:
        step_point = Point(0, Piece.PIECE_SIZE.height / 10)

    animation2 = MovementAnimation(draw_function, piece2, movement.linear_movement, final_position2, step_point)
    animation1 = MovementAnimation(draw_function, piece1, movement.linear_movement, final_position1,
                                   Point(0, 0) - step_point)

    animation1.start()
    animation2.start()

    animations.append(animation1)
    animations.append(animation2)
    return animations


def get_all_matches_on_board(board: MatchThreeBoard) -> List[Piece]:
    list_of_pieces: List[Piece] = []
    for column in board.children:
        for piece in column.children:
            list_of_pieces += board.get_match_list(piece)
    return list_of_pieces


def animate_drop(piece: Piece, final_point: Point,
                 draw_function: Callable[[], None], delay: int = 0) -> MovementAnimation:
    step_point = Point(0, Piece.PIECE_SIZE.height / 10)
    return MovementAnimation(draw_function, piece, movement.linear_movement, final_point, step_point, delay)


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
            self.__previous = position
        elif prev_square is not None and current_square is not None and prev_square == current_square:
            current_square.selected = not current_square.selected
            self.__previous = position
        elif prev_square is not None and prev_square.selected:
            if self.draw_function is not None:
                animations += animate_swap(prev_square, current_square, self.draw_function, board)

            for animation in animations:
                animation.join()

            animations.clear()
            board.swap_children(prev_square, current_square)
            board.reset_tiles()

            matches = [prev_square, current_square]
            while matches:
                # if True:
                self.handle_matches(matches, board)

                dropping_pieces = board.get_dropping_squares()
                self.drop_squares_on_board(dropping_pieces)
                matches = get_all_matches_on_board(board)
                # time.sleep(0.05)

            self.__previous = Point(0, 0)

    def handle_matches(self, pieces: List[Piece], board: MatchThreeBoard):
        animations: List[MatchAnimation] = []
        for piece in pieces:
            matches = board.get_match_list(piece)

            for match in matches:
                if match is not None:
                    animation = MatchAnimation(self.draw_function, match)
                    animation.start()

                    animations.append(animation)
        for animation in animations:
            animation.join()

    def drop_squares_on_board(self, dropping_pieces: List[Dict[Piece, Point]]):
        animations: List[MovementAnimation] = []
        for column in dropping_pieces:
            turns = len(column)
            for piece, point in column.items():
                delay = turns - int(point.y / Piece.PIECE_SIZE.height) - 1
                animations.append(animate_drop(piece, point, self.draw_function, delay * 10))
                animations[-1].start()

        for animation in animations:
            animation.join()
        animations.clear()
