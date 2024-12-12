from pathlib import Path
from collections import defaultdict

data_folder = Path(".").resolve()


def parse_data(data):
    stones = [int(d) for d in data.split()]
    return stones


def evolve_stone(stone):
    str_stone = str(stone)
    l = len(str_stone)
    if stone == 0:
        return [1]
    elif len(str_stone) % 2 == 0:
        return [int(str_stone[: l // 2]), int(str_stone[l // 2 :])]
    else:
        return [stone * 2024]


def evolve_stones_count(stone_count):
    new_count = defaultdict(int)
    for stone in stone_count:
        evolved = evolve_stone(stone)
        for number in evolved:
            new_count[number] += stone_count[stone]
    return new_count


def evolve_stones_and_count(stones, n_blinks):
    stone_count = defaultdict(int)
    for stone in stones:
        stone_count[stone] += 1
    for _ in range(n_blinks):
        stone_count = evolve_stones_count(stone_count)
    return sum([n for _, n in stone_count.items()])


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    stones = parse_data(data)

    print("Part 1")
    n_blinks = 25
    n_stones = evolve_stones_and_count(stones, n_blinks)
    print(f"There are {n_stones} stones after {n_blinks} blinks.")
    print()

    print("Part 2")
    n_blinks = 75
    n_stones = evolve_stones_and_count(stones, n_blinks)
    print(f"There are {n_stones} stones after {n_blinks} blinks.")
    print()


if __name__ == "__main__":
    main()
