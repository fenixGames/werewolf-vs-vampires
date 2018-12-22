import time
from typing import Callable

from lib.animation import Animation
from lib.game_object import GameObject
from lib.vector import Point


def linear_movement(initial_point: Point, step: Point) -> Point:
    return initial_point + step


class MovementAnimation(Animation):
    def __init__(self,
                 draw_function: Callable[[], None],
                 game_object: GameObject,
                 movement_function: Callable[[Point, Point], Point],
                 final_point: Point, step_point: Point,
                 delay: int = 0):
        """ Handles a movement event inside the game.

        :param draw_function: The function used to draw the whole screen.
        :param game_object: The object that is going to be moved.
        :param movement_function: The function used to update the current position of the object.
        :param final_point: The final position of the object.
        :param step_point: The increment to the current point in order to get to the final point.
        :param delay: The number of turns needed for the object to start moving itself.
        """
        super().__init__(draw_function)
        self.__movement_function: Callable[[Point, Point], Point] = movement_function
        self.__object: GameObject = game_object
        self.__final_point: Point = final_point
        self.__step_point: Point = step_point
        self.__delay: int = delay

    def run(self):
        while self.__object.position != self.__final_point:
            if self.__delay > 0:
                self.__delay -= 1
            else:
                self.__object.position = self.__movement_function(self.__object.position, self.__step_point)
            self.draw_screen()
            time.sleep(0.001)
