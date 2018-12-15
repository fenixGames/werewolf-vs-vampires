import pygame

from src import window, board

WIN_WIDTH = 800
WIN_HEIGHT = 900

window = window.Window(width=WIN_WIDTH, height=WIN_HEIGHT, title="Werewolves versus Vampires")
board = board.Board((0, 100), (WIN_WIDTH, WIN_HEIGHT - 100))

board.color = pygame.Color('red')
board.divide_board(160, 160, [pygame.Color('green'), pygame.Color('blue')])
window.objects.append(board)
while True:
    window.process_events()
    window.draw_window()
