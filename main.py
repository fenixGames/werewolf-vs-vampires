import pathlib

import pygame

import src.vector
from src import window, game_object, match_three_board

WIN_WIDTH = 1000
WIN_HEIGHT = 1000

window = window.Window(width=WIN_WIDTH, height=WIN_HEIGHT, title="Werewolves versus Vampires")
window.color = pygame.Color('yellow')
board_decorator: game_object.GameObject = game_object.GameObject((150, 300), (WIN_WIDTH - 300, WIN_HEIGHT - 300))
board_decorator.sprite = pathlib.Path('resources/board_decorator.png'), src.vector.Size(700, 700)

board = match_three_board.MatchThreeBoard((75, 75), (WIN_WIDTH - 450, WIN_HEIGHT - 450), 10, 10)
board.color = (0, 255, 255)
board.init_board(55, 55)

board_decorator.children.append(board)
window.objects.append(board_decorator)
while True:
    window.process_events()
    window.draw_window()
