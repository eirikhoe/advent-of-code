from pathlib import Path
import numpy as np


def _find_jolting_diffs(joltages):
    joltages = [0, *sorted(joltages)]
    joltages.append(joltages[-1] + 3)
    n = len(joltages)
    jolt_diffs = np.diff(joltages)
    return jolt_diffs, joltages, n


def find_three_one_jolt_diff_prod(joltages):
    jolt_diffs, _, n = _find_jolting_diffs(joltages)
    n_one_jolt_diffs = np.sum(jolt_diffs == 1)
    n_three_jolt_diffs = np.sum(jolt_diffs == 3)
    return n_one_jolt_diffs * n_three_jolt_diffs


def find_adapter_orderings(joltages):

    groups = []
    jolt_diffs, joltages, n = _find_jolting_diffs(joltages)
    three_jolt_diffs = jolt_diffs == 3
    splits = np.arange(1, n)
    splits = [0, *splits[three_jolt_diffs], n]

    for i, _ in enumerate(splits[:-1]):
        groups.append(joltages[splits[i] : splits[i + 1]])

    amount = 1
    for group in groups:
        amount *= do_ordering_rec(group[1:], group[0], group[-1])

    return amount


def do_ordering_rec(joltages, current, end):
    if current == end:
        return 1
    amount = 0
    for i, joltage in enumerate(joltages):
        if joltage - current > 3:
            break
        amount += do_ordering_rec(joltages[i + 1 :], joltage, end)
    return amount


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    joltages = [int(d) for d in data.split("\n")]

    print("Part 1")
    prod = find_three_one_jolt_diff_prod(joltages)
    print("The number of 1-jolt differences multiplied by the ")
    print(f"number of 3-jolt differences is {prod}")
    print()

    print("Part 2")
    n_orderings = find_adapter_orderings(joltages)
    print("The total number of distinct ways you can arrange ")
    print("the adapters to connect the charging outlet to your ")
    print(f"device is {n_orderings}")


if __name__ == "__main__":
    main()
