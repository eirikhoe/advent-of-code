from pathlib import Path
import numpy as np
import copy
import re
from collections import defaultdict

data_folder = Path(__file__).parent.resolve()


class Eris:
    def __init__(self, file):
        self.bugs = set()
        state_arr = [[ord(d) for d in list(x)] for x in file.read_text().split("\n")]
        for i, y in enumerate(state_arr):
            for j, x in enumerate(state_arr[i]):
                if state_arr[i][j] == ord("#"):
                    self.bugs.add((0, i, j))

    def find_nearby_bugs(self):
        nearby_bugs = defaultdict(lambda: 0)
        for loc in self.bugs:
            nearby_locs = [
                (loc[0], loc[1] + 1, loc[2]),
                (loc[0], loc[1] - 1, loc[2]),
                (loc[0], loc[1], loc[2] + 1),
                (loc[0], loc[1], loc[2] - 1),
            ]
            for nearby_loc in nearby_locs:
                if nearby_loc[1] == -1:
                    nearby_bugs[(loc[0] - 1, 1, 2)] += 1
                elif nearby_loc[1] == 5:
                    nearby_bugs[(loc[0] - 1, 3, 2)] += 1
                elif nearby_loc[2] == -1:
                    nearby_bugs[(loc[0] - 1, 2, 1)] += 1
                elif nearby_loc[2] == 5:
                    nearby_bugs[(loc[0] - 1, 2, 3)] += 1
                elif nearby_loc[1:] == (2, 2):
                    if loc[1:] == (1, 2):
                        for i in range(5):
                            nearby_bugs[(loc[0] + 1, 0, i)] += 1
                    elif loc[1:] == (3, 2):
                        for i in range(5):
                            nearby_bugs[(loc[0] + 1, 4, i)] += 1
                    elif loc[1:] == (2, 1):
                        for i in range(5):
                            nearby_bugs[(loc[0] + 1, i, 0)] += 1
                    elif loc[1:] == (2, 3):
                        for i in range(5):
                            nearby_bugs[(loc[0] + 1, i, 4)] += 1
                else:
                    nearby_bugs[nearby_loc] += 1
        return nearby_bugs

    def advance_state(self):
        nearby_bugs = self.find_nearby_bugs()

        old_bugs = self.bugs
        self.bugs = set()
        for loc in nearby_bugs:
            if (nearby_bugs[loc] == 1) or (
                (nearby_bugs[loc] == 2) and (loc not in old_bugs)
            ):
                self.bugs.add(loc)

    def print_state(self):
        grid_lims = [0, 0]
        for tile in self.bugs:
            if tile[0] > grid_lims[1]:
                grid_lims[1] = tile[0]
            elif tile[0] < grid_lims[0]:
                grid_lims[0] = tile[0]
        map_array = np.full((grid_lims[1] - grid_lims[0] + 1, 5, 5), 0, dtype=int)

        for bug in self.bugs:
            map_array[bug[0] - grid_lims[0], bug[1], bug[2]] = 1

        for j in range(grid_lims[0], grid_lims[1] + 1):
            array = map_array[j - grid_lims[0]]
            array[2, 2] = 2
            print(f"Grid: {j}:")
            print(
                "\n".join(
                    [
                        "".join([str(d) for d in row])
                        .replace("1", "#")
                        .replace("0", ".")
                        .replace("2", "?")
                        for row in array
                    ]
                )
            )


def main():
    file = data_folder / "day_24_input.txt"
    eris = Eris(file)
    n_min = 200
    for i in range(n_min):
        eris.advance_state()
    eris.print_state()
    print(f"After {n_min} minutes there are {len(eris.bugs)} bugs present.")


if __name__ == "__main__":
    main()

