from pathlib import Path
from collections import defaultdict
from itertools import combinations

data_folder = Path(".").resolve()


def parse_data(data):
    grid = [list(row) for row in data.split("\n")]
    size = (len(grid), len(grid[0]))
    antennas = defaultdict(list)
    for i, row in enumerate(grid):
        for j, el in enumerate(row):
            if el != ".":
                antennas[el].append((i, j))
    return size, antennas


def find_antinode_pair(pair, size):
    delta = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])
    valid_antinodes = set()
    for j in range(2):
        antinode = (pair[1 - j][0] + delta[0], pair[1 - j][1] + delta[1])
        if valid_pos(antinode, size):
            valid_antinodes.add(antinode)
        delta = (-delta[0], -delta[1])
    return valid_antinodes


def find_all_antinodes(pair, size):
    delta = (pair[1][0] - pair[0][0], pair[1][1] - pair[0][1])
    antinodes = set()
    for j in range(2):
        antinode = pair[1 - j]
        while valid_pos(antinode, size):
            antinodes.add(antinode)
            antinode = (antinode[0] + delta[0], antinode[1] + delta[1])
        delta = (-delta[0], -delta[1])
    return antinodes


def valid_pos(pos, size):
    return (0 <= pos[0] < size[0]) and (0 <= pos[1] < size[1])


def count_antinodes(size, antennas, include_resonant):
    antinodes = set()
    for freq in antennas:
        for pair in combinations(antennas[freq], 2):
            if include_resonant:
                new_antinodes = find_all_antinodes(pair, size)
            else:
                new_antinodes = find_antinode_pair(pair, size)
            antinodes = antinodes.union(new_antinodes)
    return len(antinodes)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    size, antennas = parse_data(data)

    print("Part 1")
    n_antinodes = count_antinodes(size, antennas, False)
    print(f"There are {n_antinodes} antinodes.")
    print()

    print("Part 2")
    n_antinodes = count_antinodes(size, antennas, True)
    print(f"There are {n_antinodes} antinodes with resonant harmonics included.")
    print()


if __name__ == "__main__":
    main()
