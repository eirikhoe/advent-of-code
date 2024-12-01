from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    assignments = []
    for line in data.split("\n"):
        pairs = []
        for range in line.split(","):
            assignment = [int(n) for n in range.split("-")]
            pairs.append(assignment)
        assignments.append(pairs)
    return assignments


def count_overlapping_pairs(assignments, contained):
    n_overlap = 0
    for pair in assignments:
        if (pair[0][0] == pair[1][0]) or (pair[0][1] == pair[1][1]):
            n_overlap += 1
        else:
            lowest = pair[1][0] < pair[0][0]
            n_overlap += int(pair[lowest][1] >= pair[1 - lowest][int(contained)])
    return n_overlap


def main():
    data = data_folder.joinpath("input.txt").read_text()
    assignments = parse_data(data)

    print("Part 1")
    contained_pairs = count_overlapping_pairs(assignments, True)
    print(f"The number of fully contained pairs is {contained_pairs}")
    print()

    print("Part 2")
    overlapping_pairs = count_overlapping_pairs(assignments, False)
    print(f"The number of overlapping pairs is {overlapping_pairs}")
    print()


if __name__ == "__main__":
    main()
