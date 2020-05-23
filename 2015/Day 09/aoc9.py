from pathlib import Path
import numpy as np
import copy
from itertools import permutations
import re

data_folder = Path(__file__).parent.resolve()
reg = re.compile(r"(\w+) to (\w+) = (\d+)")

class Travel:
    
    def __init__(self, data):
        distances = []
        locations = set()
        for line in data.split('\n'):
            m = reg.match(line)
            assert m is not None
            new_data = list(m.groups())
            new_data[2] = int(new_data[2])
            distances.append(new_data)
            for i in range(2):
                locations.add(new_data[i])
        self.n_locs = len(locations)
        self.locs = dict(zip(locations,np.arange(self.n_locs)))
        self.dist = self.compute_distance_matrix(distances)
        
    def compute_distance_matrix(self,distances):
        n = self.n_locs
        distance_matrix = np.zeros((n, n), dtype=int)
        for d in distances:
            i = self.locs[d[0]]
            j = self.locs[d[1]]
            distance_matrix[i, j] = d[2]
        return distance_matrix + distance_matrix.T

    def find_shortest_route(self):
        s = np.arange(self.n_locs)
        min_dist = np.inf
        for order in permutations(s):
            dist = 0
            for j in range(self.n_locs - 1):
                dist += self.dist[order[j], order[j + 1]]
            if dist < min_dist:
                min_dist = dist

        return min_dist

    def find_longest_route(self):
        s = np.arange(self.n_locs)
        max_dist = 0
        for order in permutations(s):
            dist = 0
            for j in range(self.n_locs - 1):
                dist += self.dist[order[j], order[j + 1]]
            if dist > max_dist:
                max_dist = dist

        return max_dist


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    t = Travel(data)

    print("Part 1")
    print(f"The distance of the shortest route is {t.find_shortest_route()}")
    print()

    print("Part 2")
    print(f"The distance of the longest route is {t.find_longest_route()}")


if __name__ == "__main__":
    main()
