from pathlib import Path
import re

data_folder = Path(".").resolve()
sensor_reg = re.compile(
    r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
)


def parse_data(data):
    coords = []
    for line in data.split("\n"):
        group = sensor_reg.match(line).groups()
        coords.append(
            [tuple(int(g) for g in group[:2]), tuple(int(g) for g in group[2:])]
        )
    return coords


def manhattan_distance(first, second):
    return abs(first[0] - second[0]) + abs(first[1] - second[1])


def find_ruled_out(coords, y):
    ruled_out = set()
    beacon_x = {coord[1][0] for coord in coords if coord[1][1] == y}
    for coord in coords:
        dist = manhattan_distance(coord[0], coord[1])
        y_dist = abs(coord[0][1] - y)
        x_range = dist - y_dist
        if x_range < 0:
            continue
        for x in range(coord[0][0] - x_range, coord[0][0] + x_range + 1):
            if x not in beacon_x:
                ruled_out.add(x)
    return ruled_out


def rule_out(options, ruled_out):
    new_options = []
    for option in options:
        if (ruled_out[0] > option[1]) or (ruled_out[1] < option[0]):
            new_options.append(option)
            continue
        if ruled_out[0] > option[0]:
            new_options.append([option[0], ruled_out[0] - 1])
        if ruled_out[1] < option[1]:
            new_options.append([ruled_out[1] + 1, option[1]])
    return new_options


def find_beacon_pos(coords, limits):
    options = [[[0, limits[0]]] for _ in range(limits[1] + 1)]
    for coord in coords:
        dist = manhattan_distance(coord[0], coord[1])
        for y in range(
            max(coord[0][1] - dist, 0), min(coord[0][1] + dist, limits[1]) + 1
        ):
            y_dist = abs(coord[0][1] - y)
            x_range = dist - y_dist
            options[y] = rule_out(
                options[y],
                [max(coord[0][0] - x_range, 0), min(coord[0][0] + x_range, limits[0])],
            )
    for y, option in enumerate(options):
        if (len(option) == 1) and (option[0][0] == option[0][1]):
            return (option[0][0], y)


def compute_tuning_frequency(pos):
    return 4000000 * pos[0] + pos[1]


def main():
    data = data_folder.joinpath("input.txt").read_text()
    coords = parse_data(data)

    print("Part 1")
    y = 2000000
    ruled_out = find_ruled_out(coords, y)
    print(f"{len(ruled_out)} positions at y={y} cannot contain a beacon.")
    print()

    print("Part 2")
    limit = 4000000
    beacon_pos = find_beacon_pos(coords, [limit, limit])
    tuning_frequency = compute_tuning_frequency(beacon_pos)
    print(f"The tuning frequency of the distress beacon is {tuning_frequency}.")
    print()


if __name__ == "__main__":
    main()
