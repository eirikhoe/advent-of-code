from pathlib import Path
from copy import deepcopy

data_folder = Path(".").resolve()


def operate(symb, first, second):
    if symb == "+":
        return first + second
    elif symb == "-":
        return first - second
    elif symb == "*":
        return first * second
    elif symb == "/":
        return first / second


def parse_data(data):
    unknown = dict()
    computed = dict()
    for line in data.split("\n"):
        name, val = line.split(": ")
        try:
            val = int(val)
            computed[name] = val
        except ValueError:
            first, symb, second = val.split()
            unknown[name] = (symb, first, second)
    return unknown, computed


def compute_monkey(computed, unknown, name):
    computed = deepcopy(computed)
    unknown = deepcopy(unknown)
    while name not in computed:
        to_delete = []
        for monkey in unknown:
            symb, first, second = unknown[monkey]
            if (first in computed) and (second in computed):
                computed[monkey] = operate(symb, computed[first], computed[second])
                to_delete.append(monkey)
        for monkey in to_delete:
            del unknown[monkey]
    return int(computed[name])


def search(computed, unknown):
    computed = deepcopy(computed)
    unknown = deepcopy(unknown)
    _, first, second = unknown["root"]
    unknown["root"] = ("-", first, second)
    humn_range = [1, 10]
    root_signs = [True, True]
    for i in range(2):
        computed["humn"] = humn_range[i]
        root = compute_monkey(computed, unknown, "root")
        if int(root) == 0:
            return computed["humn"]
        root_signs[i] = root > 0

    while root_signs[0] == root_signs[1]:
        humn_range = [humn_range[1], humn_range[1] * 10]
        computed["humn"] = humn_range[1]
        root = compute_monkey(computed, unknown, "root")
        if int(root) == 0:
            return computed["humn"]
        root_signs[1] = root > 0

    while humn_range[0] < humn_range[1] - 1:
        mid = (humn_range[0] + humn_range[1]) // 2
        computed["humn"] = mid
        root = compute_monkey(computed, unknown, "root")
        if int(root) == 0:
            return computed["humn"]
        root_sign = root > 0
        if root_sign == root_signs[0]:
            humn_range = [mid, humn_range[1]]
        else:
            humn_range = [humn_range[0], mid]


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    unknown, computed = parse_data(data)

    print("Part 1")
    name = "root"
    value = compute_monkey(computed, unknown, name)
    print(f"The monkey named {name} will yell the number {value}.")
    print()

    print("Part 2")
    humn_value = search(computed, unknown)
    print(f"The value we should yell to pass root's equality check is {humn_value}.")
    print()


if __name__ == "__main__":
    main()
