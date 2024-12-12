from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    equations = []
    for line in data.split("\n"):
        res, factors = line.split(":")
        res = int(res)
        factors = tuple(int(factor) for factor in factors.strip().split())
        equations.append((res, factors))
    return equations


def concat(first, second):
    return int(str(first) + str(second))


def is_solvable(res, factors, include_conc, curr=0):
    if len(factors) == 0:
        return curr == res
    elif curr > res:
        return False
    factor = factors[0]
    factors = factors[1:]
    solvable = is_solvable(res, factors, include_conc, curr + factor)
    solvable = solvable or is_solvable(res, factors, include_conc, curr * factor)
    if include_conc:
        solvable = solvable or is_solvable(
            res, factors, include_conc, concat(curr, factor)
        )
    return solvable


def find_calibration_result(equations, include_conc):
    return sum([eq[0] for eq in equations if is_solvable(eq[0], eq[1], include_conc)])


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    equations = parse_data(data)

    print("Part 1")
    cal_res = find_calibration_result(equations, False)
    print(f"The calibration result is {cal_res}.")
    print()

    print("Part 2")
    cal_res = find_calibration_result(equations, True)
    print(f"The calibration result with the concatenation operator is {cal_res}.")
    print()


if __name__ == "__main__":
    main()
