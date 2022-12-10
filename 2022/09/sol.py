from pathlib import Path
from copy import deepcopy

data_folder = Path(".").resolve()

DIRECTIONS = {"L": (0, -1), "R": (0, 1), "U": (-1, 0), "D": (1, 0)}


def parse_data(data):
    to_int = lambda x: [DIRECTIONS[x[0]], int(x[1])]
    motions = list(map(to_int, [line.split() for line in data.split("\n")]))

    return motions


def sgn(n):
    if n == 0:
        return 0
    return n // abs(n)


def _move_rope_part(head, tail):
    tail_diff = [head[i] - tail[i] for i in range(2)]
    sgn_diff = list(map(sgn, tail_diff))
    abs_diff = list(map(abs, tail_diff))
    max_abs_diff = max(abs_diff)
    new_tail = deepcopy(tail)
    if max_abs_diff < 2:
        return new_tail
    for i in range(2):
        if abs_diff[i] >= 1:
            new_tail[i] = tail[i] + sgn_diff[i]
    return new_tail


def move_rope(rope, head_direction, visited_tail):
    rope = deepcopy(rope)
    n_knots = len(rope)
    rope[0] = [rope[0][i] + head_direction[i] for i in range(2)]
    for i in range(n_knots - 1):
        rope[i + 1] = _move_rope_part(rope[i], rope[i + 1])

    visited_tail.add(tuple(rope[-1]))
    return rope, visited_tail


def find_visited_tail_positions(motions, n_knots):
    visited = {(0, 0)}
    rope = [[0, 0] for _ in range(n_knots)]
    for motion in motions:
        for _ in range(motion[1]):
            rope, visited = move_rope(rope, motion[0], visited)
    return visited


def main():
    data = data_folder.joinpath("input.txt").read_text()
    motions = parse_data(data)

    print("Part 1")
    visited = find_visited_tail_positions(motions, 2)
    print(f"The tail of the rope with two knots visited {len(visited)} positions.")
    print()

    print("Part 2")
    visited = find_visited_tail_positions(motions, 10)
    print(f"The tail of the rope with ten knots visited {len(visited)} positions.")
    print()


if __name__ == "__main__":
    main()
