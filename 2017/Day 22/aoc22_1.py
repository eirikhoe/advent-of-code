from pathlib import Path
import numpy as np
import re
from collections import defaultdict
import re

reg = re.compile(r"([#./]+) => ([#./]+)")


class Cluster:
    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    def __init__(self, data):
        self.infected = set()
        self.virus_loc = (0, 0)
        self.infectious_bursts = 0
        self.dir_index = 0

        grid = data.split("\n")

        n_rows = len(grid)
        n_cols = len(grid[0])

        if (n_rows % 2 == 0) or (n_cols % 2 == 0):
            raise RuntimeError("Starting grid has no center")

        for i, row in enumerate(grid):
            for j, char in enumerate(row):
                if char == "#":
                    self.infected.add((i - n_rows // 2, j - n_cols // 2))

    def move(self):
        if self.virus_loc in self.infected:
            self.dir_index = (self.dir_index - 1) % 4
            self.infected.remove(self.virus_loc)
        else:
            self.dir_index = (self.dir_index + 1) % 4
            self.infected.add(self.virus_loc)
            self.infectious_bursts += 1

        p = self.virus_loc
        v = Cluster.dirs[self.dir_index]
        self.virus_loc = (p[0] + v[0], p[1] + v[1])

    def evolve(self, n):
        for _ in range(n):
            self.move()

    def print_map(self):
        row_dim = [0, 0]
        column_dim = [0, 0]
        tile_rows = []
        tile_columns = []
        for tile in self.infected:
            if tile[0] > row_dim[1]:
                row_dim[1] = tile[0]
            elif tile[0] < row_dim[0]:
                row_dim[0] = tile[0]
            if tile[1] > column_dim[1]:
                column_dim[1] = tile[1]
            elif tile[1] < column_dim[0]:
                column_dim[0] = tile[1]
            tile_rows.append(tile[0])
            tile_columns.append(tile[1])

        tile_rows = np.array(tile_rows)
        tile_columns = np.array(tile_columns)
        map_array = np.full(
            (row_dim[1] - row_dim[0] + 1, 2 * (column_dim[1] - column_dim[0]) + 1),
            4,
            dtype=int,
        )
        map_array[:, ::2] = 0
        map_array[tile_rows - row_dim[0], 2 * (tile_columns - column_dim[0])] = 1
        map_array[
            self.virus_loc[0] - row_dim[0], 2 * (self.virus_loc[1] - column_dim[0]) - 1
        ] = 2
        map_array[
            self.virus_loc[0] - row_dim[0], 2 * (self.virus_loc[1] - column_dim[0]) + 1
        ] = 3
        s = "\n".join(
            [
                "".join([str(d) for d in row])
                .replace("0", ".")
                .replace("1", "#")
                .replace("2", "[")
                .replace("3", "]")
                .replace("4", " ")
                for row in map_array
            ]
        )
        print(s)


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    c = Cluster(data)
    print("Part 1")
    n_bursts = int(1e4)
    c.evolve(n_bursts)
    print(
        f"{c.infectious_bursts} bursts cause a node to become infected "
        + f"after {n_bursts} bursts of activity"
    )
    print()


if __name__ == "__main__":
    main()
