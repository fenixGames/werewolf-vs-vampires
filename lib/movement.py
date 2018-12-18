import time
from typing import Callable

from lib.animation import Animation
from lib.game_object import GameObject
from lib.vector import Point


def linear_movement(initial_point: Point, step: Point) -> Point:
    return initial_point + step


class MovementAnimation(Animation):
    def __init__(self, draw_function: Callable[[], None], game_object: GameObject,
                 movement_function: Callable[[Point, Point], Point], final_point: Point):
        super().__init__(draw_function)
        self.__movement_function: Callable[[Point, Point], Point] = movement_function
        self.__object: GameObject = game_object
        self.__final_point: Point = final_point
        self.__step_point = (final_point - game_object.position)
        self.__step_point.x /= 10
        self.__step_point.y /= 10

    def run(self):
        while self.__object.position != self.__final_point:
            print(f'{self.__object.position} -> {self.__final_point}')
            self.__object.position = self.__movement_function(self.__object.position, self.__step_point)
            self.draw_screen()
            time.sleep(0.001)
