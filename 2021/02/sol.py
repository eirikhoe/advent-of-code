from pathlib import Path

data_folder = Path(".").resolve()


move_instr = {"up": (0, -1), "down": (0, 1), "forward": (1, 1)}


def part1(data):
    pos = [0, 0]
    for direction, distance in data:
        index, unit = move_instr[direction]
        pos[index] += unit * distance
    return pos[0] * pos[1]


def part2(data):
    pos = [0, 0, 0]
    for direction, distance in data:
        index, unit = move_instr[direction]
        if index == 0:
            pos[2] += unit * distance
        else:
            pos[1] += unit * distance
            pos[0] += pos[2] * distance
    return pos[0] * pos[1]


def parse_line(line):
    direction, distance = line.split()
    distance = int(distance)
    return direction, distance


def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = [parse_line(d) for d in data.split("\n")]

    sub_prod = part1(data)
    print("Part 1")
    print(
        f"If we multiply the final horizontal position by the final depth we get {sub_prod}"
    )
    print()

    sub_prod = part2(data)
    print("Part 2")
    print(
        f"If we multiply the final horizontal position by the final depth we get {sub_prod}"
    )
    print()


if __name__ == "__main__":
    main()
