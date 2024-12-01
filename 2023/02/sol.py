from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    lines = data.split("\n")
    return lines


def find_needed_cubes_per_id(games_info, colors):
    games_needed_cubes = dict()
    for line in games_info:
        line = line[5:]
        parts = line.split(":")
        id = int(parts[0])
        games_needed_cubes[id] = dict(zip(colors, [0] * len(colors)))
        rounds = parts[1].split(";")
        for round in rounds:
            for color_info in round.split(","):
                number, color = color_info.split()
                number = int(number)
                if number > games_needed_cubes[id][color]:
                    games_needed_cubes[id][color] = number
    return games_needed_cubes


def sum_possible_games_ids(games_needed_cubes, color_limits):
    sum_possible = 0
    for id in games_needed_cubes:
        possible = True
        for color in games_needed_cubes[id]:
            if games_needed_cubes[id][color] > color_limits[color]:
                possible = False
                break
        if possible:
            sum_possible += id
    return sum_possible


def sum_games_powers(games_needed_cubes):
    sum_powers = 0
    for id in games_needed_cubes:
        power = 1
        for color in games_needed_cubes[id]:
            power *= games_needed_cubes[id][color]
        sum_powers += power
    return sum_powers


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    games_info = parse_data(data)
    color_limits = {"red": 12, "green": 13, "blue": 14}
    colors = list(color_limits.keys())
    games_needed_cubes = find_needed_cubes_per_id(games_info, colors)

    print("Part 1")
    sum_possible_ids = sum_possible_games_ids(games_needed_cubes, color_limits)
    print(f"The sum of ids of possible games is {sum_possible_ids}.")
    print()

    print("Part 2")
    sum_powers = sum_games_powers(games_needed_cubes)
    print(f"The sum of powers of all games is {sum_powers}.")
    print()


if __name__ == "__main__":
    main()
