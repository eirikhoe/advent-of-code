from pathlib import Path
import re
from copy import deepcopy
from collections import defaultdict
from bisect import bisect_left
import numpy as np


def find_allowable_ips(data):
    allowed = np.full(4294967295 + 1, True)
    for line in data.split("\n"):
        endpoints = [int(d) for d in line.split("-")]
        allowed[endpoints[0] : (endpoints[1] + 1)] = False
    return np.argmax(allowed), np.sum(allowed)


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    lowest_ip, n_ips = find_allowable_ips(data)

    print("Part 1:")
    print(f"The lowest-valued IP that is not blocked is {lowest_ip}")
    print()

    print("Part 2:")
    print(f"{n_ips} IPs are allowed by the blacklist")


if __name__ == "__main__":
    main()
