from pathlib import Path
from math import prod

data_folder = Path(".").resolve()


def total_wrapping_paper_area(data):
    area = 0
    for line in data.split("\n"):
        dimensions = [int(d) for d in line.split("x")]
        dimensions.sort()
        area += 3 * dimensions[0] * dimensions[1]
        area += 2 * dimensions[1] * dimensions[2]
        area += 2 * dimensions[2] * dimensions[0]
    return area


def total_ribbon_length(data):
    length = 0
    for line in data.split("\n"):
        dimensions = [int(d) for d in line.split("x")]
        dimensions.sort()
        length += 2 * (dimensions[0] + dimensions[1])
        length += prod(dimensions)
    return length


def main():
    data = data_folder.joinpath("input.txt").read_text()
    print("Part 1")
    area = total_wrapping_paper_area(data)
    print(f"The elves should order {area} square feet of wrapping paper in total")
    print()

    print("Part 2")
    length = total_ribbon_length(data)
    print(f"The elves should order {length} feet of ribbon in total")


if __name__ == "__main__":
    main()
