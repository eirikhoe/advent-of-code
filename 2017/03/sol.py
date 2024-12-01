from pathlib import Path
import re
from math import sqrt

data_folder = Path(".").resolve()


def man_dist(loc):
    dist = 0
    for coord in loc:
        dist += abs(coord)
    return dist


def gen_points(loc):
    points = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (i != 0) or (j != 0):
                points.append((loc[0] + i, loc[1] + j))
    return points


def gen_memory_sequence(limit):
    seq = [1]
    n = 2
    value = 1
    while value <= limit:
        loc = memory_coord(n)
        neighbours = gen_points(loc)
        circle = max(abs(loc[0]), abs(loc[1]))
        value = 0
        for neighbour in neighbours:
            if max(abs(neighbour[0]), abs(neighbour[1])) <= circle:
                index = find_n(neighbour)
                if index < n:
                    value += seq[index - 1]
        seq.append(value)
        n += 1
    return value


def find_n(loc):
    circle = max(abs(loc[0]), abs(loc[1]))
    circle_end = 1 + 4 * circle * (circle + 1)
    side_length = 2 * circle
    if loc[0] == circle:
        return circle_end - (circle - loc[1])
    elif loc[0] == -circle:
        return circle_end - 2 * side_length - (loc[1] + circle)
    elif loc[1] == -circle:
        return circle_end - side_length - (circle - loc[0])
    elif loc[1] == circle:
        return circle_end - 3 * side_length - (loc[0] + circle)


def memory_coord(n):
    circle = 1 + int(-1 + sqrt(n - 1)) // 2
    circle_end = 1 + 4 * circle * (circle + 1)
    side_length = 2 * circle
    case = (circle_end - n) // side_length
    shift = (circle_end - n) % side_length
    if case == 0:
        return (circle, circle - shift)
    elif case == 1:
        return (circle - shift, -circle)
    if case == 2:
        return (-circle, -circle + shift)
    if case == 3:
        return (-circle + shift, circle)


def main():
    square = 368078
    print("Part 1")
    print(f"{man_dist(memory_coord(square))} steps are required to carry the data")
    print()

    print("Part 2")
    print(
        f"The first value written that is larger than {square} is {gen_memory_sequence(square)}"
    )


if __name__ == "__main__":
    main()
