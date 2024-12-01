from pathlib import Path
import bisect
import copy

data_folder = Path(".").resolve()


def parse_data(data):
    galaxies = []
    for i, line in enumerate(data.split("\n")):
        for j, char in enumerate(line):
            if char == "#":
                galaxies.append([i, j])
    universe_size = [i + 1, j + 1]
    return galaxies, universe_size


def expand(galaxies, universe_size, expansion_factor=2):
    galaxies = copy.deepcopy(galaxies)
    empty_axes = []
    for k in range(2):
        filled = set([galaxy[k] for galaxy in galaxies])
        empty = sorted(list(set(range(universe_size[k])) - filled))
        empty_axes.append(empty)
    for i, galaxy in enumerate(galaxies):
        for k in range(2):
            n_offsets = bisect.bisect(empty_axes[k], galaxy[k])
            galaxies[i][k] += n_offsets * (expansion_factor - 1)
    return galaxies


def get_min_distance(first, second):
    return sum([abs(first[k] - second[k]) for k in range(2)])


def sum_min_pair_distance(galaxies):
    n_galaxies = len(galaxies)
    distance = 0
    for i in range(n_galaxies - 1):
        for j in range(i + 1, n_galaxies):
            distance += get_min_distance(galaxies[i], galaxies[j])
    return distance


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    galaxies, universe_size = parse_data(data)

    print("Part 1")
    expanded_galaxies = expand(galaxies, universe_size, expansion_factor=2)
    min_distance = sum_min_pair_distance(expanded_galaxies)
    print(
        "The sum of the minimum distance between all pairs of galaxies "
        f"after expansion is {min_distance}."
    )
    print()

    print("Part 2")
    expanded_galaxies = expand(galaxies, universe_size, expansion_factor=1_000_000)
    min_distance = sum_min_pair_distance(expanded_galaxies)
    print(
        "The sum of the minimum distance between all pairs of galaxies "
        f"after the big expansion is {min_distance}."
    )
    print()


if __name__ == "__main__":
    main()
