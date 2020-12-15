from pathlib import Path
from collections import defaultdict


def gen_final_term(start, final_length):
    seen = start[:-1]
    last_seen = dict(zip(seen, list(range(len(seen)))))
    numbers = start.copy()
    for i in range(len(seen), final_length - 1):
        if numbers[-1] in last_seen:
            val = i - last_seen[numbers[-1]]
        else:
            val = 0
        last_seen[numbers[-1]] = i
        numbers.append(val)
    return numbers[-1]


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    numbers = [int(d) for d in data.split(",")]

    print("Part 1")
    n = 2020
    end_term = gen_final_term(numbers, n)
    print(f"The {n}th number spoken will be {end_term}")
    print()

    print("Part 2")
    n = int(3e7)
    end_term = gen_final_term(numbers, n)
    print(f"The {n}th number spoken will be {end_term}")


if __name__ == "__main__":
    main()
