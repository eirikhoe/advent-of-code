from pathlib import Path
from collections import deque

data_folder = Path(".").resolve()


def parse_data(data):
    map = [[int(d) for d in line] for line in data.split("\n")]
    return map


def get_turning_dirs(dir):
    if dir[0] == 0:
        return [(1, 0), (-1, 0)]
    else:
        return [(0, 1), (0, -1)]


def valid_pos(pos, map):
    return (0 <= pos[0] < len(map)) and (0 <= pos[1] < len(map[0]))


def update_pos(pos, dir):
    return tuple([pos[k] + dir[k] for k in range(2)])


def get_cands(curr, map, ultra):
    cands = []
    pos = curr[0]
    dir = curr[1]
    turning_dirs = get_turning_dirs(dir)
    if not ultra:
        straight_lim = 3
        turning_lim = 0
    else:
        straight_lim = 10
        turning_lim = 4
    if curr[2] >= turning_lim:
        for new_dir in turning_dirs:
            new_pos = update_pos(pos, new_dir)
            if not valid_pos(new_pos, map):
                continue
            heat_loss = curr[3] + map[new_pos[0]][new_pos[1]]
            cands.append((new_pos, new_dir, 1, heat_loss))
    if curr[2] < straight_lim:
        new_pos = update_pos(pos, dir)
        if not valid_pos(new_pos, map):
            return cands
        heat_loss = curr[3] + map[new_pos[0]][new_pos[1]]
        cands.append((new_pos, dir, curr[2] + 1, heat_loss))
    return cands


def iter(pos, map, length):
    additional_heat = 0
    additional_heat += sum([map[pos[0]][pos[1] + (i + 1)] for i in range(length)])
    additional_heat += sum(
        [map[pos[0] + (i + 1)][pos[1] + length] for i in range(length)]
    )
    new_pos = (pos[0] + length, pos[1] + length)
    return additional_heat, new_pos


def naive_sol(map, ultra):
    assert len(map) == len(map[0])
    n = len(map)
    start = (0, 0)
    end = (len(map) - 1, len(map[0]) - 1)
    if not ultra:
        return sum([map[i][i] + map[i - 1][i] for i in range(1, n)])
    remainder = (n - 1) % 4
    heat_loss, pos = iter(start, map, 4 + remainder)
    while pos != end:
        additional_heat_loss, pos = iter(pos, map, 4)
        heat_loss += additional_heat_loss
    return heat_loss


def find_minimal_heat_loss(map, ultra):
    seen = dict()
    search = deque()
    start = (0, 0)
    turning_lim = 0
    straight_lim = 3
    if ultra:
        turning_lim = 4
        straight_lim = 10
    end = (len(map) - 1, len(map[0]) - 1)
    for dir in [(0, 1), (1, 0)]:
        search.appendleft((start, dir, 0, 0))
    min_heat_loss = naive_sol(map, ultra)
    while len(search) > 0:
        curr = search.pop()
        if curr[3] >= min_heat_loss:
            continue
        if (curr[0] == end) and (curr[3] < min_heat_loss) and (curr[2] >= turning_lim):
            min_heat_loss = curr[3]
        if (curr[:-1] in seen) and (curr[3] >= seen[curr[:-1]]):
            continue
        seen[curr[:-1]] = curr[3]
        if curr[2] >= turning_lim:
            for i in range(curr[2] + 1, straight_lim + 1):
                val = (curr[0], curr[1], i)
                if (val not in seen) or (curr[3] < seen[val]):
                    seen[val] = curr[3]
        cands = get_cands(curr, map, ultra)
        for cand in cands:
            search.appendleft(cand)
    return min_heat_loss


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    map_data = parse_data(data)

    print("Part 1")
    ultra = False
    min_heat_loss = find_minimal_heat_loss(map_data, ultra)
    print(f"The minimum heat loss with regular crucibles is {min_heat_loss}.")
    print()

    print("Part 2")
    ultra = True
    min_heat_loss = find_minimal_heat_loss(map_data, ultra)
    print(f"The minimum heat loss with ultra crucibles is {min_heat_loss}.")
    print()


if __name__ == "__main__":
    main()
