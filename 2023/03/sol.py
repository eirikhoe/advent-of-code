from pathlib import Path
from collections import defaultdict

data_folder = Path(".").resolve()


def parse_data(data):
    data = [list(line) for line in data.split("\n")]
    return data


def is_symbol(element, is_strict):
    if is_strict:
        return element == "*"
    return (not element.isnumeric()) and (element != ".")


def check_for_symbol(data, row, col, strict=False):
    positions = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if (
                (not ((i == 0) and (j == 0)))
                and (0 <= (row + i) < len(data))
                and (0 <= col + j < len(data[i]))
            ):
                positions.append((row + i, col + j))
    valid_pos = []
    for pos in positions:
        if is_symbol(data[pos[0]][pos[1]], strict):
            valid_pos.append(pos)
    return valid_pos


def sum_part_numbers(data):
    on_number = False
    is_part_number = False
    curr_number = ""
    part_number_sum = 0
    for row, line in enumerate(data):
        for col, element in enumerate(line):
            is_numeric = element.isnumeric()
            if is_numeric:
                curr_number += element
                if not on_number:
                    on_number = True
                is_part_number |= len(check_for_symbol(data, row, col, False)) > 0
            if ((not is_numeric) or (col == len(line) - 1)) and on_number:
                if is_part_number:
                    part_number_sum += int(curr_number)
                on_number = False
                is_part_number = False
                curr_number = ""
    return part_number_sum


def sum_gear_ratios(data):
    on_number = False
    adjacent_gear_ratios = []
    curr_number = ""
    adjacent_numbers = defaultdict(list)
    for row, line in enumerate(data):
        for col, element in enumerate(line):
            is_numeric = element.isnumeric()
            if is_numeric:
                curr_number += element
                if not on_number:
                    on_number = True
                adjacent_gear_ratios.extend(check_for_symbol(data, row, col, True))
            if ((not is_numeric) or (col == len(line) - 1)) and on_number:
                number = int(curr_number)
                adjacent_gear_ratios = list(set(adjacent_gear_ratios))
                for gear_ratio_pos in adjacent_gear_ratios:
                    adjacent_numbers[gear_ratio_pos].append(number)
                on_number = False
                adjacent_gear_ratios = []
                curr_number = ""
    gear_sum = 0
    for gear, numbers in adjacent_numbers.items():
        if len(numbers) == 2:
            gear_sum += numbers[0] * numbers[1]
    return gear_sum


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    data = parse_data(data)

    print("Part 1")
    print(f"The sum of the part numbers is {sum_part_numbers(data)}.")
    print()

    print("Part 2")
    print(f"The sum of the gear ratios is {sum_gear_ratios(data)}.")
    print()


if __name__ == "__main__":
    main()
