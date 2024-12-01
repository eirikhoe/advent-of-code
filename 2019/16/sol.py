from pathlib import Path
import numpy as np
import copy
import time
import os
from colorama import init
from math import ceil, floor

init()
data_folder = Path(__file__).parent.resolve()
start_time = time.perf_counter()


def fft(digits, repetitions, phases, use_offset=False):
    if use_offset:
        offset = int(("").join([str(d) for d in digits[:7]]))
    else:
        offset = 0

    digits = np.tile(digits, repetitions)
    n = len(digits)
    pattern = [0, 1, 0, -1]
    m = len(pattern)
    method_lim = 9 * ceil(np.sqrt(n + 1))
    offset_lim = floor(n / 2)
    if offset >= offset_lim:
        index = np.arange(n - 1, offset - 1, -1)
    else:
        first_index = np.arange(n - 1, offset_lim - 1, -1)
        second_index = np.arange(offset_lim - 1, method_lim - 1, -1)
    for k in np.arange(phases):
        old_digits = copy.deepcopy(digits)
        if offset >= offset_lim:
            digits[index] = np.cumsum(old_digits[index], dtype=int)
            digits[index] = np.mod(digits[index], 10)
        else:
            digits[first_index] = np.cumsum(old_digits[first_index], dtype=int)
            for i in second_index:
                digits[i] = digits[i + 1]
                lims = np.arange(i, n, i + 1)
                for j, lim in enumerate(lims):
                    if ((j + 1) % 4) < 2:
                        digits[i] += np.sum(old_digits[lim : lim + j + 1])
                    else:
                        digits[i] -= np.sum(old_digits[lim : lim + j + 1])

            for i in np.arange(method_lim):
                n_tiles = ceil((n + 1) / (m * (i + 1)))
                coef = np.tile(np.repeat(pattern, i + 1), n_tiles)[1 : n + 1]
                digits[i] = np.dot(coef, old_digits)
            digits = np.mod(np.abs(digits), 10)
    return "".join([str(d) for d in digits[offset : offset + 8]])


def main():
    file = data_folder / "input.txt"
    digits = np.array([int(d) for d in list(file.read_text())])

    print("Part 1")
    print(fft(digits, 1, 100, False))
    print()

    print("Part 2")
    print(fft(digits, 10000, 100, True))


if __name__ == "__main__":
    main()
