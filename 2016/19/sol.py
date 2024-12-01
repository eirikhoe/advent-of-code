import numpy as np


def last_elf_left(n_elves):
    elves = np.arange(1, n_elves + 1)
    while elves.size > 1:
        if (elves.size % 2) == 0:
            elves = elves[::2]
        else:
            elves = elves[2::2]
    return elves[0]


def last_elf_across(n_elves):
    elves = np.arange(1, n_elves + 1)
    while elves.size > 1:
        if (elves.size % 2) == 1:
            mid = elves.size // 2
            indexes = np.r_[1:mid, mid + 1 : elves.size, 0]
        else:
            n = elves.size // 2
            t = n % 3
            p = n + (n // 3)
            k = 3 * ((p - 1) // 2) + ((p - 1) % 2)
            s = (1 + n + k) % elves.size
            indexes = np.r_[(2 - t) : s : 3, s:n, n + 2 : elves.size : 3]
        elves = elves[indexes]
    return elves[0]


def main():
    n_elves = 3004953
    print("Part 1")
    print(f"Elf {last_elf_left(n_elves)} gets the last present")
    print()

    print("Part 2")
    print(f"Elf {last_elf_across(n_elves)} gets the last present")


if __name__ == "__main__":
    main()
