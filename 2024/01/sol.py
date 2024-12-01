from pathlib import Path
from collections import defaultdict

data_folder = Path(".").resolve()


def parse_data(data):
    loc_ids = [[int(d) for d in line.split()] for line in data.split("\n")]
    loc_ids = [list(l) for l in zip(*loc_ids)]
    return loc_ids


def calculate_distance(loc_ids):
    sorted_ids = [sorted(l) for l in loc_ids]
    total_distance = 0
    for i in range(len(sorted_ids[0])):
        total_distance += abs(sorted_ids[0][i] - sorted_ids[1][i])
    return total_distance


def calculate_similarity_score(loc_ids):
    id_count = defaultdict(int)
    for l in loc_ids[1]:
        id_count[l] += 1
    similarity_score = 0
    for l in loc_ids[0]:
        similarity_score += l * id_count[l]
    return similarity_score


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    loc_ids = parse_data(data)

    print("Part 1")
    total_distance = calculate_distance(loc_ids)
    print(f"The total distance is {total_distance}")
    print()

    print("Part 2")
    similarity_score = calculate_similarity_score(loc_ids)
    print(f"The similarity score is {similarity_score}")
    print()


if __name__ == "__main__":
    main()
