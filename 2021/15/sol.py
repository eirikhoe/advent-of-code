from pathlib import Path
from typing import Tuple, ClassVar
import numpy as np
from dataclasses import dataclass
from copy import deepcopy
from time import perf_counter
import bisect

data_folder = Path(".").resolve()


def parse_data(data):
    scan = [[int(d) for d in line] for line in data.split("\n")]
    return scan


def make_big_scan(scan):
    dup_factor = 5
    s = (len(scan), len(scan[0]))
    new_size = (s[0] * dup_factor, s[1] * dup_factor)
    big_scan = [[0 for _ in range(new_size[1])] for __ in range(new_size[0])]
    for i in range(dup_factor):
        for j in range(dup_factor):
            for k in range(s[0]):
                for l in range(s[1]):
                    big_scan[k + i * s[0]][l + j * s[1]] = 1 + (
                        (scan[k][l] + i + j - 1) % 9
                    )
    return big_scan


def get_candidates(pos, scan):
    candidates = []
    if pos[0] < len(scan) - 1:
        candidates.append((pos[0] + 1, pos[1], pos[2] + scan[pos[0] + 1][pos[1]]))
    if pos[1] < len(scan[0]) - 1:
        candidates.append((pos[0], pos[1] + 1, pos[2] + scan[pos[0]][pos[1] + 1]))
    if pos[0] > 0:
        candidates.append((pos[0] - 1, pos[1], pos[2] + scan[pos[0] - 1][pos[1]]))
    if pos[1] > 0:
        candidates.append((pos[0], pos[1] - 1, pos[2] + scan[pos[0]][pos[1] - 1]))
    return candidates


def find_cave_path(scan):
    pos = (0, 0, 0)
    queue = get_candidates(pos, scan)
    queue.sort(key=lambda x: x[2], reverse=False)
    seen = [[False for i in range(len(scan[0]))] for j in range(len(scan))]
    seen[0][0] = True
    for cand in queue:
        seen[cand[0]][cand[1]] = True
    while queue:
        cand = queue.pop(0)
        if (cand[0] == len(scan) - 1) and (cand[1] == len(scan[0]) - 1):
            return cand[2]
        seen[cand[0]][cand[1]] = True
        new_cands = get_candidates(cand, scan)
        for new_cand in new_cands:
            if not seen[new_cand[0]][new_cand[1]]:
                better = True
                for q in queue:
                    if (q[0], q[1]) == (new_cand[0], new_cand[1]):
                        if q[2] <= new_cand[2]:
                            better = False
                            break
                        else:
                            queue.remove(q)
                if better:
                    ind = bisect.bisect_left(queue, new_cand[2], key=lambda x: x[2])
                    queue.insert(ind, new_cand)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    scan = parse_data(data)

    print("Part 1")
    min_risk_level = find_cave_path(scan)
    print("The lowest total risk of any path from the top left to the bottom right is")
    print(f"{min_risk_level}")
    print()

    print("Part 2")
    big_scan = make_big_scan(scan)
    min_risk_level = find_cave_path(big_scan)
    print("The lowest total risk of any path from the top left to the bottom right is")
    print(f"{min_risk_level} for the full map")
    print()


if __name__ == "__main__":
    main()
