from pathlib import Path
from collections import defaultdict
import re

data_folder = Path(".").resolve()


def parse_data(data):
    sections = data.split("\n\n")
    _, seeds = sections[0].split(":")
    seeds = [int(d) for d in seeds.strip().split()]
    maps_names = dict()
    maps = defaultdict(list)
    for section in sections[1:]:
        lines = section.split("\n")
        categories = lines[0].split()[0]
        source_cat, _, destination_cat = categories.split("-")
        maps_names[source_cat] = destination_cat
        for line in lines[1:]:
            numbers = [int(d) for d in line.split()]
            maps[source_cat].append(numbers)
    return seeds, maps_names, maps


def map_category(source_number, map):
    for rule in map:
        if rule[1] <= source_number < rule[1] + rule[2]:
            return source_number + (rule[0] - rule[1])
    return source_number


def map_seed_to_location(seed_number, maps_names, maps):
    source_cat = "seed"
    destination_cat = "location"
    cat = source_cat
    number = seed_number
    while cat != destination_cat:
        map = maps[cat]
        number = map_category(number, map)
        cat = maps_names[cat]
    return number


def find_minimum_location_seed(seeds, maps_names, maps):
    min_location = None
    for seed_number in seeds:
        location = map_seed_to_location(seed_number, maps_names, maps)
        if (not min_location) or (location < min_location):
            min_location = location
    return min_location


def find_minimum_location_seed_range(seeds, maps_names, maps):
    source_cat = "seed"
    destination_cat = "location"
    cat = source_cat
    ranges = seeds
    while cat != destination_cat:
        map = maps[cat]
        ranges = map_category_ranges(ranges, map)
        cat = maps_names[cat]
    return ranges[0]


def map_category_ranges(source_ranges, map):
    destination_ranges = []
    for i in range(0, len(source_ranges), 2):
        destination_ranges.extend(map_category_range(source_ranges[i : i + 2], map))
    destination_ranges.sort(key=lambda x: x[0])
    final_ranges = []
    for i in range(1, len(destination_ranges)):
        if (
            destination_ranges[i - 1][0] + destination_ranges[i - 1][1]
        ) < destination_ranges[i][0]:
            final_ranges.extend(destination_ranges[i - 1])
        else:
            diff = destination_ranges[i][0] - destination_ranges[i - 1][0]
            destination_ranges[i][0] = destination_ranges[i - 1][0]
            destination_ranges[i][1] += diff
    final_ranges.extend(destination_ranges[-1])
    return final_ranges


def map_category_range(source_range, map):
    ranges = [source_range]
    destination_ranges = []
    for rule in map:
        new_ranges = []
        for curr_range in ranges:
            start = curr_range[0]
            end = curr_range[0] + curr_range[1]
            if (end <= rule[1]) or (start >= (rule[1] + rule[2])):
                new_ranges.append(curr_range)
                continue
            start = max(start, rule[1])
            end = min(end, rule[1] + rule[2])
            delta = rule[0] - rule[1]
            destination_ranges.append([start + delta, end - start])
            if curr_range[0] < start:
                new_ranges.append([curr_range[0], start - curr_range[0]])
            if (curr_range[0] + curr_range[1]) > end:
                new_ranges.append([end, curr_range[0] + curr_range[1] - end])
        ranges = new_ranges
    for curr_range in ranges:
        destination_ranges.append(curr_range)
    return destination_ranges


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    seeds, maps_names, maps = parse_data(data)

    print("Part 1")
    min_location = find_minimum_location_seed(seeds, maps_names, maps)
    print(f"The minimum location for a seed is {min_location}.")
    print()

    print("Part 2")
    min_location = find_minimum_location_seed_range(seeds, maps_names, maps)
    print(f"The minimum location for the range of seeds is {min_location}.")
    print()


if __name__ == "__main__":
    main()
