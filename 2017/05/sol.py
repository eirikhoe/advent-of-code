from pathlib import Path
import re

data_folder = Path(".").resolve()


def main():
    data = data_folder.joinpath("input.txt").read_text()
    jumps = []
    for line in data.split("\n"):
        jumps.append(int(line))

    org_jumps = jumps.copy()
    print("Part 1")

    n_offsets = len(jumps)
    n_steps = 0
    index = 0
    while index < n_offsets:
        jump = jumps[index]
        jumps[index] += 1
        index += jump
        n_steps += 1

    print(f"It takes {n_steps} steps to to reach the exit")
    print()

    print("Part 2")
    jumps = org_jumps.copy()
    n_steps = 0
    index = 0
    while index < n_offsets:
        jump = jumps[index]
        if jumps[index] < 3:
            jumps[index] += 1
        else:
            jumps[index] -= 1
        index += jump
        n_steps += 1

    print(f"It takes {n_steps} steps to to reach the exit")
    print()


if __name__ == "__main__":
    main()
