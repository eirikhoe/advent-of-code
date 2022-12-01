from pathlib import Path

data_folder = Path(".").resolve()

def parse_data(data):
    elves = data.split("\n\n")
    elves = [[int(food) for food in elf.split("\n")] for elf in elves]
    return elves


def main():
    data = data_folder.joinpath("input.txt").read_text()
    elves = parse_data(data)
    sorted_total_calories = sorted(map(sum,elves))

    print("Part 1")
    print(sorted_total_calories[-1])

    print("Part 2")
    print(sum(sorted_total_calories[-3:]))


if __name__ == "__main__":
    main()
