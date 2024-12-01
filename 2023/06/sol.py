from pathlib import Path
import math

data_folder = Path(".").resolve()


def parse_data(data):
    lines = data.split("\n")
    parsed_lines = []
    for line in lines:
        _, line = line.split(":")
        line = [int(d) for d in line.strip().split()]
        parsed_lines.append(line)
    times = parsed_lines[0]
    record_distances = parsed_lines[1]
    return times, record_distances


def compute_winning_ways(time, record_distance):
    middle = time / 2
    delta = math.sqrt(((time**2) / 4) - record_distance)

    low_lim = math.floor(middle - delta) + 1
    high_lim = math.ceil(middle + delta) - 1

    return high_lim - low_lim + 1


def compute_total_winning_ways(times, record_distances):
    ways = 1
    for i, _ in enumerate(times):
        ways *= compute_winning_ways(times[i], record_distances[i])
    return ways


def merge_numbers(number_list):
    new_number = int("".join([str(d) for d in number_list]))
    return new_number


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    times, record_distances = parse_data(data)

    print("Part 1")
    winning_ways = compute_total_winning_ways(times, record_distances)
    print(f"The number of ways to win all races is {winning_ways}.")
    print()

    print("Part 2")
    record_distance, time = map(merge_numbers, (record_distances, times))
    winning_ways = compute_winning_ways(time, record_distance)
    print(f"The number of ways to win the one big race is {winning_ways}.")
    print()


if __name__ == "__main__":
    main()
