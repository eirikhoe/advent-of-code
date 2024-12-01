from pathlib import Path
from collections import deque, defaultdict
import copy

data_folder = Path(".").resolve()

beam_symb = {(0, 1): ">", (0, -1): "<", (1, 0): "v", (-1, 0): "^"}


def parse_data(data):
    contraption = [list(row) for row in data.split("\n")]
    return contraption


def draw_lit_contraption(contraption, lights):
    s = ""
    for i, _ in enumerate(contraption):
        for j, tile in enumerate(contraption[i]):
            if (tile == ".") and ((i, j) in lights):
                l = list(lights[(i, j)])
                if len(l) == 1:
                    s += beam_symb[l[0]]
                else:
                    s += str(len(l))
            else:
                s += contraption[i][j]
        s += "\n"
    return s


def advance_beam(init_beam, contraption):
    lights = defaultdict(set)
    unfinished = deque([init_beam])
    while len(unfinished) > 0:
        curr = unfinished.pop()
        pos = curr[0]
        dir = curr[1]
        if dir in lights[pos]:
            continue
        symb = contraption[pos[0]][pos[1]]
        cands = step(symb, pos, dir)
        for cand in cands:
            if (0 <= cand[0][0] < len(contraption)) and (
                0 <= cand[0][1] < len(contraption[0])
            ):
                unfinished.appendleft(cand)
        lights[curr[0]].add(curr[1])
    return lights


def count_energized_tiles(lights):
    return len(lights)


def update_pos(pos, dir):
    return tuple([pos[k] + dir[k] for k in range(2)])


def step(symb, pos, dir):
    new_dirs = []
    match (symb, dir[0], dir[1]):
        case (".", _, _) | ("-", 0, _) | ("|", _, 0):
            new_dirs.append(dir)
        case ("-", _, 0):
            for i in [-1, 1]:
                new_dir = (0, i)
                new_dirs.append(new_dir)
        case ("|", 0, _):
            for i in [-1, 1]:
                new_dir = (i, 0)
                new_dirs.append(new_dir)
        case ("/", 0, 1) | ("\\", 0, -1):
            new_dirs.append((-1, 0))
        case ("/", 0, -1) | ("\\", 0, 1):
            new_dirs.append((1, 0))
        case ("/", 1, 0) | ("\\", -1, 0):
            new_dirs.append((0, -1))
        case ("/", -1, 0) | ("\\", 1, 0):
            new_dirs.append((0, 1))
    return [(update_pos(pos, d), d) for d in new_dirs]


def find_most_energized(contraption):
    beams = []
    for i, _ in enumerate(contraption):
        n = len(contraption)
        beams.extend([((i, n - 1), (0, -1)), ((i, 0), (0, 1))])
    for j, _ in enumerate(contraption[0]):
        n = len(contraption[0])
        beams.extend([((n - 1, j), (-1, 0)), ((0, j), (1, 0))])
    max_energized = 0
    for beam in beams:
        lights = advance_beam(beam, contraption)
        n_energized = count_energized_tiles(lights)
        if n_energized > max_energized:
            max_energized = n_energized

    return max_energized


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    contraption = parse_data(data)

    print("Part 1")
    init_beam = ((0, 0), (0, 1))
    lights = advance_beam(init_beam, contraption)
    n_energized = count_energized_tiles(lights)
    print(f"{n_energized} tiles end up being energized.")
    print()

    print("Part 2")
    max_energized = find_most_energized(contraption)
    print(
        f"{max_energized} tiles end up being energized when using "
        "the optimal configuration."
    )
    print()


if __name__ == "__main__":
    main()
