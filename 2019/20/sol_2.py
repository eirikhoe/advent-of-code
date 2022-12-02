from pathlib import Path
import numpy as np
import copy

data_folder = Path(__file__).parent.resolve()


class Portal:
    def __init__(self, name, outer):
        self.name = name
        self.destination = None
        self.outer = outer


class Maze:
    """A Maze class"""

    def __init__(self, map_file):
        map = [[ord(d) for d in list(x)] for x in map_file.read_text().split("\n")]
        self.map = np.array(map, dtype=int)
        self.portals, self.start, self.end = self.get_portals()

    def get_portals(self):
        portals = dict()
        s_y = self.map.shape[0]
        s_x = self.map.shape[1]
        for y in np.arange(s_y):
            for x in np.arange(s_x):
                if ord("A") <= self.map[y, x] <= ord("Z"):
                    for candidate in [(y, x + 1), (y + 1, x)]:
                        if (
                            (candidate[0] < s_y)
                            and (candidate[1] < s_x)
                            and (ord("A") <= self.map[candidate] <= ord("Z"))
                        ):
                            name = chr(self.map[y, x]) + chr(self.map[candidate])
                            entrance = (
                                candidate[0] + (candidate[0] - y),
                                candidate[1] + (candidate[1] - x),
                            )
                            if (
                                (entrance[0] < s_y)
                                and (entrance[1] < s_x)
                                and (self.map[entrance] == ord("."))
                            ):
                                point = entrance
                            else:
                                point = (y - (candidate[0] - y), x - (candidate[1] - x))

                            if name == "AA":
                                start = point
                            elif name == "ZZ":
                                end = point
                            else:
                                other_loc = None
                                for loc in portals:
                                    if portals[loc].name == name:
                                        other_loc = loc
                                        break
                                if (
                                    (point[0] == 2)
                                    or (point[0] == s_y - 3)
                                    or (point[1] == 2)
                                    or (point[1] == s_x - 3)
                                ):
                                    is_outer = True
                                else:
                                    is_outer = False
                                portals[point] = Portal(name, is_outer)
                                if other_loc is not None:
                                    portals[other_loc].destination = point
                                    portals[point].destination = other_loc

        return portals, start, end

    def find_exit(self):
        distance = np.full(self.map.shape, -2, dtype=int)
        distance[self.map == ord(".")] = -1
        distance = np.reshape(distance, (1, *distance.shape))
        init_distance = distance.copy()
        distance[0][self.start] = 0
        queue = [(0, *self.start)]
        while len(queue) > 0:
            point = queue.pop(0)
            for candidate in [
                (point[0], point[1], point[2] + 1),
                (point[0], point[1], point[2] - 1),
                (point[0], point[1] + 1, point[2]),
                (point[0], point[1] - 1, point[2]),
            ]:
                if (distance[candidate] == -1) and self.map[candidate[1:]] == ord("."):
                    queue.append(candidate)
                    distance[candidate] = distance[point] + 1
                elif candidate[0] == 0:
                    if (ord("A") <= self.map[candidate[1:]] <= ord("Z")) and (
                        point[1:] != self.start
                    ):
                        if self.end == point[1:]:
                            return distance[point]
                        else:
                            if not self.portals[point[1:]].outer:
                                if distance.shape[0] == candidate[0] + 1:
                                    distance = np.concatenate(
                                        [distance, init_distance], axis=0
                                    )
                                potential_point = (
                                    point[0] + 1,
                                    *self.portals[point[1:]].destination,
                                )
                                if distance[potential_point] < 0:
                                    queue.append(potential_point)
                                    distance[potential_point] = distance[point] + 1
                else:
                    if ord("A") <= self.map[candidate[1:]] <= ord("Z"):
                        if (self.end != point[1:]) and (self.start != point[1:]):
                            if not self.portals[point[1:]].outer:
                                if distance.shape[0] == candidate[0] + 1:
                                    distance = np.concatenate(
                                        [distance, init_distance], axis=0
                                    )
                                potential_point = (
                                    point[0] + 1,
                                    *self.portals[point[1:]].destination,
                                )
                            else:
                                potential_point = (
                                    point[0] - 1,
                                    *self.portals[point[1:]].destination,
                                )
                            if distance[potential_point] < 0:
                                queue.append(potential_point)
                                distance[potential_point] = distance[point] + 1


def main():
    file = data_folder / "input.txt"
    maze = Maze(file)
    print(f"It takes {maze.find_exit()} steps to reach the ZZ exit.")


if __name__ == "__main__":
    main()
