from pathlib import Path
import re
import copy
import math

data_folder = Path(".").resolve()
reg = re.compile(r"([\?\.#]+) (\d+(?:,\d+)*)")


def parse_data(data):
    info = []
    for line in data.split("\n"):
        groups = reg.match(line).groups()
        ranges = tuple(int(d) for d in groups[1].split(","))
        info.append([list(groups[0]), ranges])
    return info


def find_valid_permutations(row, copies):
    criteria = list(row[1])
    orig_record = row[0]

    # Simplify all cases of more than one working spring in a row
    # Same solution as with just one
    record = [orig_record[0]]
    for char in orig_record[1:]:
        if not (char == record[-1] == "."):
            record.append(char)

    # Duplicate
    orig_criteria = copy.deepcopy(criteria)
    orig_record = copy.deepcopy(record)
    for _ in range(1, copies):
        criteria += orig_criteria
        record += ["?", *orig_record]

    return base_solve(record, criteria)


def base_solve(record, criteria):
    # Solve by divide and conquer

    # Check if we can return immediately
    if len(record) == 0:
        res = int(len(criteria) == 0)
        return res
    if len(criteria) == 0:
        if "#" in record:
            return 0
        else:
            return 1
    deg_freedom = len(record) - (sum(criteria) - 1)
    if deg_freedom < len(criteria):
        return 0

    n_valid = 0
    # Split on first known working spring if possible
    split = False
    for i, char in enumerate(record):
        if char != ".":
            continue
        split = True
        j = 0
        while (j <= len(criteria)) and (sum(criteria[:j]) + (j - 1) <= i):
            if sum(criteria[j:]) + (len(criteria) - j - 1) > len(record) - i - 1:
                j += 1
                continue
            partial_valid = base_solve(record[:i], criteria[:j])
            if partial_valid > 0:
                partial_valid *= base_solve(record[i + 1 :], criteria[j:])
            n_valid += partial_valid
            j += 1
        break
    if split:
        return n_valid

    # No workings springs, so split on first known faulty if possible
    split = False
    for i, char in enumerate(record):
        if char == "?":
            continue
        split = True
        size = 1
        for k in range(i + 1, len(record)):
            if record[k] != "#":
                break
            size += 1
        for j, crit in enumerate(criteria):
            initial_gap = int(j > 0)
            final_gap = int(j < (len(criteria) - 1))
            if crit < size:
                continue
            slack = crit - size
            start = max(i - slack, initial_gap)
            end = min(i + 1, len(record) - crit + 1 - final_gap)
            if start >= end:
                continue
            for k in range(start, end):
                if (bool(initial_gap) and (record[k - 1] == "#")) or (
                    bool(final_gap) and (record[k + crit] == "#")
                ):
                    continue
                partial_valid = base_solve(record[: k - initial_gap], criteria[:j])
                if partial_valid > 0:
                    partial_valid *= base_solve(
                        record[k + crit + final_gap :], criteria[j + 1 :]
                    )
                n_valid += partial_valid
        break
    if split:
        return n_valid

    # All unknown springs so can solve using combinatorics
    return math.comb(deg_freedom, len(criteria))


def sum_valid_permutations(info, copies):
    func = lambda info: find_valid_permutations(info, copies)
    return sum(map(func, info))


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    info = parse_data(data)

    print("Part 1")
    print(sum_valid_permutations(info, copies=1))
    print()

    print("Part 2")
    print(sum_valid_permutations(info, copies=5))
    print()


if __name__ == "__main__":
    main()
