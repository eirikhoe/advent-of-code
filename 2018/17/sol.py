from pathlib import Path
import numpy as np
import re
from bisect import bisect_left
from copy import deepcopy
from itertools import compress

reg = re.compile(r"(y|x)=(\d+), (y|x)=(\d+)\.\.(\d+)")


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    res = Reservoir(data)
    res.flow()
    res.print_ground()
    print(f"The water can reach {res.count_water()} tiles")
    print(f"There are {res.count_rest_water()} tiles left after the spring stops.")


class Reservoir:
    def __init__(self, data):
        data = data.split("\n")

        ax = {"x": 1, "y": 0}
        sep = ".."
        for i, line in enumerate(data):
            m = reg.match(line).group(1, 2, 3, 4, 5)
            data[i] = [[], []]
            data[i][ax[m[0]]] = [int(m[1])]
            data[i][ax[m[2]]] = [int(m[3]), int(m[4])]

        self.lims = [[0, 0], [500, 500]]
        self.lowest_y = None
        for line in data:
            for j, dim in enumerate(line):
                for point in dim:
                    if point > self.lims[j][1]:
                        self.lims[j][1] = point

                    if point < self.lims[j][0]:
                        self.lims[j][0] = point

                    if (j == 0) and (
                        (self.lowest_y is None) or (point < self.lowest_y)
                    ):
                        self.lowest_y = point

        self.lims[1][0] -= 1
        self.lims[1][1] += 1

        self.size = (self.lims[0][1] + 1, self.lims[1][1] - self.lims[1][0] + 1)

        self.ground = np.full(self.size, ord("."), dtype=int)
        for line in data:
            if len(line[1]) == 2:
                self.ground[
                    line[0][0],
                    (line[1][0] - self.lims[1][0]) : (line[1][1] + 1 - self.lims[1][0]),
                ] = ord("#")
            else:
                self.ground[
                    line[0][0] : (line[0][1] + 1), line[1][0] - self.lims[1][0]
                ] = ord("#")

        self.spring = (0, 500 - self.lims[1][0])
        self.ground[self.spring[0], self.spring[1]] = ord("+")
        self.flowing = [self.spring]

    def print_ground(self):
        s = ""
        col_size = self.lims[1][1]
        col_digits = len(str(col_size))
        row_size = self.lims[0][1]
        row_digits = len(str(row_size))

        form_str = "{:" + str(col_digits) + "d}"
        for j in range(col_digits):
            s += " " * row_digits
            for loc in range(self.lims[1][0], self.lims[1][1] + 1):
                loc_str = form_str.format(loc)
                s += loc_str[j]
            s += "\n"

        form_str = "{:" + str(row_digits) + "d}"
        for y in range(row_size + 1):
            s += form_str.format(y)
            for k in self.ground[y]:
                s += chr(k)
            s += "\n"
        data_folder = Path(".").resolve()
        data_folder.joinpath("output.txt").write_text(s)

    def flow_step(self):
        active = [True] * len(self.flowing)
        active_len = len(active)
        for j, tile in enumerate(self.flowing):
            if active[j]:
                below = (tile[0] + 1, tile[1])
                left = (tile[0], tile[1] - 1)
                right = (tile[0], tile[1] + 1)
                if below[0] >= self.size[0]:
                    active[j] = False
                elif self.ground[below] == ord("."):
                    self.ground[below] = ord("|")
                    self.flowing.append(below)
                    active.append(True)
                elif self.ground[below] in [ord("~"), ord("#")]:
                    i_l = 1
                    left_below = (tile[0] + 1, tile[1] - i_l)
                    while (self.ground[left] in [ord("."), ord("|")]) and (
                        self.ground[left_below] in [ord("~"), ord("#")]
                    ):
                        i_l += 1
                        left = (tile[0], tile[1] - i_l)
                        left_below = (tile[0] + 1, tile[1] - i_l)

                    i_r = 1
                    right_below = (tile[0] + 1, tile[1] + i_r)
                    while (self.ground[right] in [ord("."), ord("|")]) and (
                        self.ground[right_below] in [ord("~"), ord("#")]
                    ):
                        i_r += 1
                        right = (tile[0], tile[1] + i_r)
                        right_below = (tile[0] + 1, tile[1] + i_r)

                    if (self.ground[right] == ord("#")) and (
                        self.ground[left] == ord("#")
                    ):
                        self.ground[tile[0], (left[1] + 1) : right[1]] = ord("~")
                        for k, _ in enumerate(active):
                            if (self.flowing[k][0] == tile[0]) and (
                                left[1] < self.flowing[k][1] < right[1]
                            ):
                                active[k] = False
                    else:
                        closed_left = int(self.ground[left] not in [ord("."), ord("|")])
                        open_right = int(self.ground[right] in [ord("."), ord("|")])
                        self.ground[
                            tile[0], (left[1] + closed_left) : (right[1] + open_right)
                        ] = ord("|")
                        if not closed_left:
                            self.flowing.append(left)
                            active.append(True)
                        if open_right:
                            self.flowing.append(right)
                            active.append(True)
                        active[j] = False

        self.flowing = list(compress(self.flowing, active))

        return (len(active) != active_len) or (sum(active) != active_len)

    def flow(self):
        while self.flow_step():
            pass

    def count_water(self):
        return np.sum(np.isin(self.ground[self.lowest_y :], [ord("|"), ord("~")]))

    def count_rest_water(self):
        return np.sum(self.ground[self.lowest_y :] == ord("~"))


if __name__ == "__main__":
    main()
