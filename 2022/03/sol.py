from pathlib import Path
import string

data_folder = Path(".").resolve()
type_to_priority = dict(zip(string.ascii_letters, range(1, 53)))


def parse_data(data):
    rucksacks = [[type_to_priority[l] for l in line] for line in data.split("\n")]
    return rucksacks


def find_common_type(rucksack):
    comp_size = len(rucksack) // 2
    common = list(set.intersection(set(rucksack[:comp_size]), set(rucksack[comp_size:])))[0]
    return common


def sum_elf_group_priorities(rucksacks):
    n_rucksacks = len(rucksacks)
    group_size = 3
    badge_priorities = []
    for group_id in range(0, n_rucksacks, group_size):
        group = [set(rucksack) for rucksack in rucksacks[group_id : group_id + group_size]]
        common = list(set.intersection(*group))[0]
        badge_priorities.append(common)
    return sum(badge_priorities)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    rucksacks = parse_data(data)

    print("Part 1")
    priorities_sum = sum([find_common_type(rucksack) for rucksack in rucksacks])
    print(f"The sum of priorities of the common item types in both compartments is {priorities_sum}")

    print("Part 2")
    priorities_sum = sum_elf_group_priorities(rucksacks)
    print(f"The sum of priorities of the common item types for each elf group is {priorities_sum}")


if __name__ == "__main__":
    main()
