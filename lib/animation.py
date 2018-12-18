import threading
from typing import Callable


class Animation(threading.Thread):
    def __init__(self, draw_function: Callable[[], None]):
        super().__init__()
        self.__draw_function: Callable[[], None] = draw_function

    @property
    def draw_function(self) -> Callable[[], None]:
        return self.__draw_function

    def run(self):
        pass
