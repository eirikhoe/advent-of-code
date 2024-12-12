from pathlib import Path
import re

data_folder = Path(".").resolve()


def parse_data(data):
    reg = re.compile(r"mul\(\d+,\d+\)|do\(\)|don't\(\)")
    instr_strings = reg.findall(data)
    instrs = []
    for s in instr_strings:
        if s == "do()":
            instrs.append(True)
        elif s == "don't()":
            instrs.append(False)
        else:
            core = s[4:-1]
            factors = tuple(int(d) for d in core.split(","))
            instrs.append(factors)
    return instrs


def get_multiplication_sum(instrs, include_conditional):
    prod_sum = 0
    do_mul = True
    for instr in instrs:
        if isinstance(instr, bool):
            do_mul = instr
        elif (not include_conditional) or do_mul:
            prod_sum += instr[0] * instr[1]
    return prod_sum


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    instrs = parse_data(data)

    print("Part 1")
    mult_sum = get_multiplication_sum(instrs, False)
    print(f"The multiplication sum is {mult_sum}.")
    print()

    print("Part 2")
    mult_sum = get_multiplication_sum(instrs, True)
    print(f"The multiplication sum with conditional statements included is {mult_sum}.")
    print()


if __name__ == "__main__":
    main()
