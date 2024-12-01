from pathlib import Path
import numpy as np
import re
from collections import deque

data_folder = Path(".").resolve()


def dist(pos_a, pos_b):
    d = 0
    for i in range(4):
        d += abs(pos_a[i] - pos_b[i])
    return d


def main():
    data = data_folder.joinpath("input.txt").read_text()
    points = []
    for line in data.split("\n"):
        points.append([int(d) for d in line.split(",")])

    constellations = []
    for i, point in enumerate(points):
        belongs_to = []
        for j, constellation in enumerate(constellations):
            for k in constellation:
                if dist(point, points[k]) <= 3:
                    belongs_to.append(j)
                    break

        if len(belongs_to) == 0:
            constellations.append([i])
        else:
            for red in belongs_to[-1:0:-1]:
                constellations[belongs_to[0]] += constellations.pop(red)
            constellations[belongs_to[0]].append(i)

    # for j,constellation in enumerate(constellations):
    #     print(f"Constellation {j}")
    #     for point in constellation:
    #         print(point)

    print(
        f"{len(constellations)} constellations are formed by the fixed points in spacetime"
    )


if __name__ == "__main__":
    main()
