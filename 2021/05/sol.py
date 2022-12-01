from pathlib import Path
from numpy.lib.twodim_base import diag
from numpy.ma.core import count
import parse
import numpy as np

data_folder = Path(".").resolve()


def parse_data(data):
    lines = []
    line_parse = parse.compile("{},{} -> {},{}")
    for line in data.split("\n"):
        lines.append([int(d) for d in line_parse.parse(line).fixed])
    return np.array(lines, dtype=int)


def count_overlap_points(lines, include_diag):
    grid = np.zeros((np.max(lines[:, [0, 2]]) + 1, np.max(lines[:, [1, 3]]) + 1), dtype=int)

    horisontal = np.equal(lines[:, 1], lines[:, 3])
    hor_rows = lines[horisontal]
    for row in hor_rows:
        row_lim = np.sort(row[[0, 2]])
        row_lim[1] += 1
        grid[row[1], row_lim[0] : row_lim[1]] += 1

    vertical = np.equal(lines[:, 0], lines[:, 2])
    ver_rows = lines[vertical]
    for row in ver_rows:
        row_lim = np.sort(row[[1, 3]])
        row_lim[1] += 1
        grid[row_lim[0] : row_lim[1], row[0]] += 1

    if include_diag:
        diag_rows = lines[np.logical_not(np.logical_or(horisontal, vertical))]
        for row in diag_rows:
            ind = np.argsort(row[[0, 2]])
            x = row[[0, 2]][ind]
            y = row[[1, 3]][ind]
            slope = 1 if y[1] > y[0] else -1
            for i in range(1 + x[1] - x[0]):
                grid[y[0] + i * slope, x[0] + i] += 1

    return np.sum(grid >= 2)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = parse_data(data)

    print("Part 1")
    n_overlap = count_overlap_points(data, False)
    print(f"At least two lines overlap in {n_overlap} points when not including diagonal lines")
    print()

    print("Part 2")
    n_overlap = count_overlap_points(data, True)
    print(f"At least two lines overlap in {n_overlap} points when including diagonal lines")
    print()


if __name__ == "__main__":
    main()
