from pathlib import Path
import copy
from collections import defaultdict

maxx = 0
level_counter = defaultdict(int)

data_folder = Path(".").resolve()

valid_dirs = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


def parse_data(data):
    trails = [list(line) for line in data.split("\n")]
    return trails


def valid_pos(pos, map):
    return (0 <= pos[0] < len(map)) and (0 <= pos[1] < len(map[0]))


def update_pos(pos, dir):
    return tuple([pos[k] + dir[k] for k in range(2)])


def get_cands(pos, trails, uphill, seen=None):
    if seen is None:
        seen = set()
    cands = []
    for dir in ((0, 1), (0, -1), (-1, 0), (1, 0)):
        cand = update_pos(pos, dir)
        if not valid_pos(cand, trails):
            continue
        plot = trails[cand[0]][cand[1]]
        if (
            (
                (not uphill)
                and (
                    (plot == ".")
                    or ((plot in valid_dirs) and (valid_dirs[plot] == dir))
                )
            )
            or (uphill and (plot != "#"))
        ) and (cand not in seen):
            cands.append(cand)
    return cands


def make_path_map(trails, uphill):
    start_pos = (0, 1)
    path_map = defaultdict(dict)
    for i, _ in enumerate(trails):
        for j, _ in enumerate(trails[0]):
            pos = (i, j)
            if trails[i][j] == "#":
                continue
            cands = get_cands(pos, trails, True)
            if (len(cands) <= 2) and (pos != start_pos):
                continue
            for cand in cands:
                res = walk_until_split(trails, pos, cand, uphill)
                if (res is not None) and (
                    (res[0] not in path_map[pos]) or (res[1] > path_map[pos][res[0]])
                ):
                    path_map[pos][res[0]] = res[1]
    return path_map


def walk_until_split(trails, origin, start, uphill):
    seen = set([origin])
    size = (len(trails), len(trails[0]))
    pos = start
    dist = 1
    while True:
        seen.add(pos)
        cands = get_cands(pos, trails, uphill, seen)
        if (len(cands) > 1) or (pos == (size[0] - 1, size[1] - 2)):
            return (pos, dist)
        elif len(cands) == 0:
            return None
        pos = cands[0]
        dist += 1


def print_trails(trails, seen):
    s = ""
    for i, _ in enumerate(trails):
        for j, _ in enumerate(trails[0]):
            if (i, j) in seen:
                s += "O"
            else:
                s += trails[i][j]
        s += "\n"
    print(s)


def take_step(path_map, pos, end, seen, curr_path_length):
    seen = copy.deepcopy(seen)
    seen.add(pos)
    if pos == end:
        return curr_path_length
    max_path_length = 0
    for cand in path_map[pos]:
        if cand in seen:
            continue
        new_length = curr_path_length + path_map[pos][cand]
        path_length = take_step(path_map, cand, end, seen, new_length)
        if path_length > max_path_length:
            max_path_length = path_length
    return max_path_length


def find_longest_path(trails, uphill):
    start = (0, 1)
    size = (len(trails), len(trails[0]))
    end = (size[0] - 1, size[1] - 2)
    path_map = make_path_map(trails, uphill)
    return take_step(path_map, start, end, set(), 0)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    trails = parse_data(data)

    print("Part 1")
    longest_path = find_longest_path(trails, uphill=False)
    print(f"The longest path if we can't walk up slopes is {longest_path} steps.")
    print()

    print("Part 2")
    longest_path = find_longest_path(trails, uphill=True)
    print(f"The longest path if we can walk up slopes is {longest_path} steps.")
    print()


if __name__ == "__main__":
    main()
