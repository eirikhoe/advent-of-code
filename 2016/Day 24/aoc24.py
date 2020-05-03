from pathlib import Path
import numpy as np
import copy
import time
from itertools import permutations

data_folder = Path(__file__).parent.resolve()


class Duct:
    def __init__(self, map_file):
        map = [[ord(d) for d in list(x)] for x in map_file.read_text().split("\n")]
        self.map = np.array(map, dtype=np.int8)
        self.locs = self.get_locs()
        self.n_locs = len(self.locs)
        self.dist = self.compute_distance_matrix()

    def get_locs(self):
        locs_dict = dict()
        for y in np.arange(self.map.shape[0]):
            for x in np.arange(self.map.shape[1]):
                if ord("0") <= self.map[y, x] <= ord("9"):
                    self.map[y, x] = int(chr(self.map[y, x]))
                    locs_dict[self.map[y, x]] = (y, x)

        locs = [[]] * len(locs_dict)
        for index in locs_dict:
            locs[index] = locs_dict[index]
        return locs

    def bfs(self, pos):
        distance = np.full(self.map.shape, -1, dtype=int)
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
                if (distance[candidate] < 0) and self.map[candidate] != ord("#"):
                    queue.append(candidate)
                    distance[candidate] = distance[point] + 1
        return distance

    def compute_distance_matrix(self):
        n = self.n_locs
        distance_matrix = np.zeros((n, n), dtype=int)
        for i in range(n - 1):
            distance = self.bfs(self.locs[i])
            for j in range(i + 1, n):
                distance_matrix[i, j] = distance[self.locs[j]]
        return distance_matrix + distance_matrix.T

    def find_min_dist(self, back_to_start=False):
        s = np.arange(1, self.n_locs)
        min_dist = np.inf
        for order in permutations(s):
            dist = 0
            order = (0, *order)
            for j in range(self.n_locs - 1):
                dist += self.dist[order[j], order[j + 1]]
            if back_to_start:
                dist += self.dist[order[self.n_locs - 1], 0]
            if dist < min_dist:
                min_dist = dist

        return min_dist


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt")
    d = Duct(data)

    print("Part 1")
    print(f"It takes {d.find_min_dist()} steps to visit all locations")
    print()

    print("Part 2")
    print(
        f"It takes {d.find_min_dist(True)} steps to visit all locations and return to start"
    )


if __name__ == "__main__":
    main()
