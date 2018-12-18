import threading
from typing import Callable


class Animation(threading.Thread):
    LOCK = threading.Lock()

    def __init__(self, draw_function: Callable[[], None]):
        super().__init__()
        self.__draw_function: Callable[[], None] = draw_function

    def draw_screen(self):
        if self.LOCK.acquire(blocking=False):
            self.__draw_function()
            self.LOCK.release()

    def run(self):
        pass
