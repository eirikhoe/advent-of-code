from pathlib import Path
import numpy as np
import copy
import time
from collections import deque
data_folder = Path(__file__).parent.resolve()


class Maze:
    """A Maze class"""

    def __init__(self, number):
        self.fav_number = number
        self.pos = (1,1)

    def min_path(self, endpoint):
        distance = {self.pos:0}
        queue = deque([self.pos])
        while len(queue) > 0:
            point = queue.pop()
            for candidate in [
                (point[0], point[1] + 1),
                (point[0], point[1] - 1),
                (point[0] + 1, point[1]),
                (point[0] - 1, point[1]),
            ]:
                if ((min(candidate) >= 0) and (candidate not in distance)) and self.open(candidate):
                    queue.appendleft(candidate)
                    distance[candidate] = distance[point] + 1
                    if candidate == endpoint:
                        return distance[endpoint]
        return None

    def reachable_locs(self, max_dist):
        distance = {self.pos:0}
        unique_locs = 1
        queue = deque([self.pos])
        while len(queue) > 0:
            point = queue.pop()
            if distance[point] < max_dist:
                for candidate in [
                    (point[0], point[1] + 1),
                    (point[0], point[1] - 1),
                    (point[0] + 1, point[1]),
                    (point[0] - 1, point[1]),
                ]:
                    if ((min(candidate) >= 0) and (candidate not in distance)) and self.open(candidate):
                        queue.appendleft(candidate)
                        distance[candidate] = distance[point] + 1
                        unique_locs += 1
        return unique_locs

    def open(self,point):
        x,y = point
        value = x*x + 3*x + 2*x*y + y + y*y
        value += self.fav_number
        bin_value = bin(value)[2:]
        value = sum([int(d=='1') for d in bin_value]) % 2
        return value == 0        


def main():
    fav_number = 1364
    maze = Maze(fav_number)
    point = (31,39)
    print('Part 1')
    print(f"It takes a minimum of {maze.min_path(point)} steps to reach {str(point)[1:-1]}")
    print()

    print('Part 2')
    max_dist = 50
    print(f"You can reach {maze.reachable_locs(max_dist)} locations in at most {max_dist} steps")


if __name__ == "__main__":
    main()
