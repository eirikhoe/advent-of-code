from pathlib import Path
from collections import defaultdict

data_folder = Path(".").resolve()

WIRES_TO_DIGIT = {
    "abcefg": "0",
    "cf": "1",
    "acdeg": "2",
    "acdfg": "3",
    "bcdf": "4",
    "abdfg": "5",
    "abdefg": "6",
    "acf": "7",
    "abcdefg": "8",
    "abcdfg": "9",
}


def parse_data(data):
    digits_list = []
    display_list = []
    for line in data.split("\n"):
        digits, display = line.split("|")
        digits = [d for d in digits.split()]
        display = [d for d in display.split()]
        digits_list.append(digits)
        display_list.append(display)
    return digits_list, display_list


def read_digits(digits, display):
    wrong_to_right = dict()
    n_wires = defaultdict(lambda: [])
    wire_sets = dict()

    for digit in digits:
        n = len(digit)
        n_wires[n].append(set(digit))
    wire_sets["a"] = n_wires[3][0] - n_wires[2][0]
    cf = n_wires[3][0] - wire_sets["a"]
    bd = n_wires[4][0] - cf
    eg = n_wires[7][0] - (set.union(wire_sets["a"], cf, bd))
    cde = set()
    for digit in n_wires[6]:
        cde = set.union(cde, n_wires[7][0] - digit)
    wire_sets["c"] = set.intersection(cde, cf)
    wire_sets["f"] = cf - wire_sets["c"]
    wire_sets["d"] = set.intersection(cde, bd)
    wire_sets["b"] = bd - wire_sets["d"]
    wire_sets["e"] = set.intersection(cde, eg)
    wire_sets["g"] = eg - wire_sets["e"]
    for wire in wire_sets:
        wrong_to_right[set_to_str(wire_sets[wire])] = wire
    output_digits = ""
    for wires in display:
        correct_wires = []
        for wire in wires:
            correct_wires.append(wrong_to_right[wire])
        correct_wires = "".join(sorted(correct_wires))
        output_digits += WIRES_TO_DIGIT[correct_wires]
    return output_digits


def count_digit_appearances(digits, displays):
    n_appear = 0
    for digit, display in zip(digits, displays):
        output_digits = read_digits(digit, display)
        for digit in output_digits:
            if digit in ["1", "4", "7", "8"]:
                n_appear += 1
    return n_appear


def sum_output_values(digits, displays):
    n = 0
    for digit, display in zip(digits, displays):
        output_digits = read_digits(digit, display)
        n += int(output_digits)
    return n


def set_to_str(s):
    return list(s)[0]


def main():
    data = data_folder.joinpath("input.txt").read_text()
    digits_list, display_list = parse_data(data)

    print("Part 1")
    n_digit_appearances = count_digit_appearances(digits_list, display_list)
    print(f"In the output values, the digits 1, 4, 7, or 8 appear {n_digit_appearances} times.")
    print()

    print("Part 2")
    number_sum = sum_output_values(digits_list, display_list)
    print(f"We get {number_sum} if we sum up all the output_values.")
    print()


if __name__ == "__main__":
    main()
