from pathlib import Path
from collections import defaultdict


def gen_final_term(numbers, n_turns):
    last_seen = {n: i for i, n in enumerate(numbers[:-1], start=1)}
    prev = numbers[-1]
    for i in range(len(numbers), n_turns):
        n = i - last_seen.get(prev, i)
        last_seen[prev] = i
        prev = n
    return n


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
