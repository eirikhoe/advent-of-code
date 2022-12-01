from pathlib import Path
import numpy as np
import copy

data_folder = Path(__file__).parent.resolve()


class Portal:
    def __init__(self, name):
        self.name = name
        self.destination = None


class Maze:
    """A Maze class"""

    def __init__(self, map_file):
        map = [[ord(d) for d in list(x)] for x in map_file.read_text().split("\n")]
        self.map = np.array(map, dtype=int)
        self.portals = self.get_portals()

    def get_portals(self):
        portals = dict()
        for y in np.arange(self.map.shape[0]):
            for x in np.arange(self.map.shape[1]):
                if ord("A") <= self.map[y, x] <= ord("Z"):
                    for candidate in [(y, x + 1), (y + 1, x)]:
                        if (
                            (candidate[0] < self.map.shape[0])
                            and (candidate[1] < self.map.shape[1])
                            and (ord("A") <= self.map[candidate] <= ord("Z"))
                        ):
                            name = chr(self.map[y, x]) + chr(self.map[candidate])
                            entrance = (
                                candidate[0] + (candidate[0] - y),
                                candidate[1] + (candidate[1] - x),
                            )
                            if (
                                (entrance[0] < self.map.shape[0])
                                and (entrance[1] < self.map.shape[1])
                                and (self.map[entrance] == ord("."))
                            ):
                                point = entrance
                            else:
                                point = (y - (candidate[0] - y), x - (candidate[1] - x))
                            other_loc = None
                            for loc in portals:
                                if portals[loc].name == name:
                                    other_loc = loc
                                    break
                            portals[point] = Portal(name)
                            if other_loc is not None:
                                portals[other_loc].destination = point
                                portals[point].destination = other_loc

        return portals

    def find_exit(self, pos):
        distance = np.full(self.map.shape, -2, dtype=int)
        distance[self.map == ord(".")] = -1
        distance[pos] = 0
        queue = [pos]
        while len(queue) > 0:
            point = queue.pop(0)
            for candidate in [
                (point[0], point[1] + 1),
                (point[0], point[1] - 1),
                (point[0] + 1, point[1]),
                (point[0] - 1, point[1]),
            ]:
                if (distance[candidate] == -1) and self.map[candidate] == ord("."):
                    queue.append(candidate)
                    distance[candidate] = distance[point] + 1
                elif (ord("A") <= self.map[candidate] <= ord("Z")) and (pos != point):
                    if self.portals[point].name == "ZZ":
                        return distance[point]
                    elif distance[self.portals[point].destination] < 0:
                        queue.append(self.portals[point].destination)
                        distance[self.portals[point].destination] = distance[point] + 1


def main():
    file = data_folder / "day_20_input.txt"
    maze = Maze(file)

    for key in maze.portals:
        # print(maze.portals[key].destination)
        if maze.portals[key].name == "AA":
            print(f"It takes {maze.find_exit(key)} steps to reach the ZZ exit.")


if __name__ == "__main__":
    main()
