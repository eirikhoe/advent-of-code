from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    garden = [list(line) for line in data.split("\n")]
    for i, line in enumerate(garden):
        for j, char in enumerate(line):
            if char == "S":
                garden[i][j] = "."
                return garden, (i, j)


def valid_pos(pos, map):
    return (0 <= pos[0] < len(map)) and (0 <= pos[1] < len(map[0]))


def update_pos(pos, dir):
    return tuple([pos[k] + dir[k] for k in range(2)])


def get_cands(pos, garden):
    cands = []
    for dir in ((0, 1), (0, -1), (-1, 0), (1, 0)):
        cand = update_pos(pos, dir)
        if valid_pos(cand, garden) and (garden[cand[0]][cand[1]] == "."):
            cands.append(cand)
    return cands


def _base_reachable_fun(garden, start_pos, n_steps):
    new_reachable = [1]
    seen = set([start_pos])
    search = [start_pos]
    for i in range(n_steps):
        new_search = []
        while len(search) > 0:
            pos = search.pop()
            cands = get_cands(pos, garden)
            for cand in cands:
                if cand not in seen:
                    new_search.append(cand)
                    seen.add(cand)
        new_reachable.append(len(new_search))
        search = new_search
        if len(search) == 0:
            break
    start_ind = n_steps % 2
    return sum(new_reachable[start_ind::2]), i


def find_max_dist_seen(garden, start_pos, n_steps):
    _, max_dist = _base_reachable_fun(garden, start_pos, n_steps)
    return max_dist


def find_n_reachable_pos(garden, start_pos, n_steps):
    n_reachable, _ = _base_reachable_fun(garden, start_pos, n_steps)
    return n_reachable


def find_n_reachable_grid(garden, n_steps):
    # square garden
    assert len(garden) == len(garden[0])

    map_len = len(garden)

    # odd map length
    assert map_len % 2 == 1

    mid = (map_len - 1) // 2

    # steps are exactly such that we end up at the edge of
    # the base map in every cardinal direction
    assert (n_steps % map_len) == (map_len - 1) / 2
    n_copies = n_steps // map_len

    # No obstacles from the starting point in the cardinal
    # directions
    for i in range(map_len):
        assert garden[mid][i] == "."
        assert garden[i][mid] == "."

    # we can reach every reachable spot on every copy of the map
    # where all its points are at most n_steps from the starting
    # pos
    max_dist = find_max_dist_seen(garden, (mid, mid), map_len)
    assert max_dist == (map_len - 1)

    reachable_unit = [0, 0]
    reachable_unit[0] = find_n_reachable_pos(garden, (mid, mid), 2 * map_len)
    reachable_unit[1] = find_n_reachable_pos(garden, (mid, mid), 2 * map_len - 1)

    central_parity = n_steps % 2
    if ((n_copies - 1) % 2) == 1:
        dominant_parity = 1 - central_parity
    else:
        dominant_parity = central_parity

    # Interior
    n_reachable = reachable_unit[dominant_parity] * (n_copies**2)
    n_reachable += reachable_unit[1 - dominant_parity] * ((n_copies - 1) ** 2)

    # Points
    for s in [(0, mid), (map_len - 1, mid), (mid, 0), (mid, map_len - 1)]:
        n_reachable += find_n_reachable_pos(garden, s, map_len - 1)

    # Edges
    for s in [(0, map_len - 1), (0, 0), (map_len - 1, 0), (map_len - 1, map_len - 1)]:
        n_reachable += n_copies * find_n_reachable_pos(garden, s, mid - 1)
        n_reachable += (n_copies - 1) * find_n_reachable_pos(garden, s, 3 * mid)

    return n_reachable


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    garden, start_pos = parse_data(data)

    print("Part 1")
    n_steps = 64
    n_reachable = find_n_reachable_pos(garden, start_pos, n_steps)
    print(f"The elf can reach {n_reachable} garden plots in {n_steps} steps.")
    print()

    print("Part 2")
    n_steps = 26501365
    n_reachable = find_n_reachable_grid(garden, n_steps)
    print(f"The elf can reach {n_reachable} garden plots in {n_steps} steps.")
    print()


if __name__ == "__main__":
    main()
