from collections import deque
import copy
from hashlib import md5
from pathlib import Path
import time

import numpy as np

data_folder = Path(__file__).parent.resolve()

def gen_grid(initial_line,n_lines):
    symbols = {'.':0,'^':1}
    curr = np.array([symbols[d] for d in initial_line],dtype=int)
    prev = np.zeros(curr.size+2,dtype=int)
    n_safe = np.sum(curr==0)
    for i in np.arange(n_lines-1):
        prev[1:-1] =  np.copy(curr)
        curr = np.logical_xor(prev[:-2],prev[2:]).astype(int)
        n_safe += np.sum(curr==0)

    return n_safe


def main():
    data = data_folder.joinpath("input.txt").read_text()
    
    print("Part 1")
    n_rows = 40
    print(f"There are {gen_grid(data,n_rows)} safe tiles in {n_rows} rows")
    print()

    print("Part 2")
    n_rows = 400000
    print(f"There are {gen_grid(data,n_rows)} safe tiles in {n_rows} rows")


if __name__ == "__main__":
    main()
