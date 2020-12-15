from mazegenerator import Maze
import numpy as np


class WallFollower:
    def __init__(self, maze_obj, follow_left=False):
        self.maze = maze_obj.maze
        self.size = maze_obj.size
        self.follow_left = follow_left
        self.coords = (0, 1)
        self.destination = (self.size - 1, self.size - 2)
        self.path = [self.coords]
        self._direction = 180
        self._direct_map = {
            0: np.array([0, -1]),
            90: np.array([-1, 0]),
            180: np.array([0, 1]),
            270: np.array([1, 0])
        }

    def is_path_in_front(self):
        new_coords = tuple(self.coords + self._direct_map[self._direction])
        return (self.maze[new_coords] == Maze.PATH).all()

    def turn_right(self):
        self._direction += 90
        self._direction %= 360

    def turn_left(self):
        self._direction -= 90
        self._direction %= 360

    def turn(self):
        if self.follow_left:
            self.turn_left()
        else:
            self.turn_right()

    def step(self):
        self.coords = self.coords + self._direct_map[self._direction]
        self.coords = tuple(self.coords)

    def move(self):
        if self.coords != self.destination:
            if self.follow_left:
                self.turn_left()
            else:
                self.turn_right()

            if self.is_path_in_front():
                self.step()
                return

            for _ in range(3):
                if self.follow_left:
                    self.turn_right()
                else:
                    self.turn_left()

                if self.is_path_in_front():
                    self.step()
                    return
