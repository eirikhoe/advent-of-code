from pathlib import Path
import numpy as np
from itertools import product

data_folder = Path(".").resolve()


def _get_selection(dir, size):
    if dir == 0:
        return (0, size, 0, size)
    elif dir == 1:
        return (0, size - 1, 1, size)
    elif dir == -1:
        return (1, size, 0, size - 1)


def parse_data(data):
    octopi = [[int(d) for d in line] for line in data.split("\n")]
    octopi = np.array(octopi, dtype=int)
    return octopi


def sim_octopi(octopi):
    octopi += 1
    not_counted = np.full_like(octopi, fill_value=True, dtype=bool)
    add_increase = 1
    while add_increase > 0:
        increase = np.zeros_like(octopi)
        for dir in product([-1, 0, 1], repeat=2):
            if dir == (0, 0):
                continue
            row_sel = _get_selection(dir[0], octopi.shape[0])
            col_sel = _get_selection(dir[1], octopi.shape[1])
            octopi_sel = octopi[row_sel[2] : row_sel[3], col_sel[2] : col_sel[3]]
            selected_sel = not_counted[row_sel[2] : row_sel[3], col_sel[2] : col_sel[3]]
            check_sel = increase[row_sel[0] : row_sel[1], col_sel[0] : col_sel[1]]
            check_sel += np.logical_and((octopi_sel > 9), selected_sel)
        not_counted[octopi > 9] = False
        octopi += increase
        add_increase = np.sum(increase)
    octopi[octopi > 9] = 0
    return octopi


def find_first_all_flash(octopi):
    octopi = np.copy(octopi)
    i = 0
    while np.sum(octopi) > 0:
        octopi = sim_octopi(octopi)
        i += 1
    return i


def count_flashes(octopi, n_steps):
    n_flashes = 0
    octopi = np.copy(octopi)
    for i in range(n_steps):
        octopi = sim_octopi(octopi)
        n_flashes += np.sum(octopi == 0)
    return n_flashes


def print_octopi(octopi, step):
    s = f"After step {step}:\n"
    for line in octopi:
        for octopus in line:
            s += str(octopus)
        s += "\n"
    print(s)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    octopi = parse_data(data)

    print("Part 1")
    n = 100
    print(f"There are {count_flashes(octopi, n)} total flashes after {n} steps")
    print()

    print("Part 2")
    print(f"All octopi flash after {find_first_all_flash(octopi)} steps")
    print()


if __name__ == "__main__":
    main()
