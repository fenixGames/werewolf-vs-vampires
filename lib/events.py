import sys
from typing import List, Any, Callable

import pygame


class Event:
    def __init__(self, type: pygame.event.EventType, args: Any = None):
        self.__type: pygame.event.EventType = type
        self.__args: Any = args
        self.__draw_function: Callable[[None], None] = None

    @property
    def type(self) -> pygame.event.EventType:
        return self.__type

    @property
    def args(self):
        return self.__args

    @property
    def draw_function(self) -> Callable[[None], None]:
        return self.__draw_function

    @draw_function.setter
    def draw_function(self, value: Callable[[None], None]):
        self.__draw_function = value

    def handle(self, event: pygame.event.Event):
        pass


class ExitEvent(Event):
    def __init__(self):
        super().__init__(pygame.QUIT)

    def handle(self, event: pygame.event.Event):
        sys.exit()


class EventHandler:
    def __init__(self):
        self.__event_list: List[Event] = []

    @property
    def events(self) -> List[Event]:
        return self.__event_list

    def check_events(self, game_events: List[pygame.event.Event]):
        for game_event in game_events:
            for event in self.events:
                if event.type == game_event.type:
                    event.handle(game_event)
