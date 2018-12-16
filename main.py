import pathlib

import pygame

import lib.vector
import src
from lib import events, game_object, graphics, window, vector
from src import board

WIN_WIDTH = 700
WIN_HEIGHT = 1000

window = window.Window(width=WIN_WIDTH, height=WIN_HEIGHT, title="Werewolves versus Vampires")
window.color = pygame.Color('yellow')
board_decorator: game_object.GameObject = game_object.GameObject((0, 300), (WIN_WIDTH, WIN_HEIGHT - 300))
board_decorator.sprite = graphics.GraphicResource(pathlib.Path('resources/board_decorator.png'),
                                                  lib.vector.Size(700, 700)), lib.vector.Size(700, 700)

board = board.MatchThreeBoard((75, 75), (WIN_WIDTH - 150, WIN_HEIGHT - 450), 10, 10)
# board.color = (0, 255, 255)
board.init_board(55, 55)

board_decorator.children.append(board)
window.objects.append(board_decorator)

event_handler = events.EventHandler()
event_handler.events.append(events.ExitEvent())
click_event = src.events.MouseButtonDownEvent(board, vector.Point(0, 300))
click_event.draw_function = window.draw_window
event_handler.events.append(click_event)
while True:
    event_handler.check_events(pygame.event.get())
    window.draw_window()
