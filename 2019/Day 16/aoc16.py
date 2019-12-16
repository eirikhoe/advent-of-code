from pathlib import Path
import numpy as np
import copy
import time
import os
from colorama import init
from math import ceil
init()
data_folder = Path(__file__).parent.resolve()





def main(): 
    file = data_folder / "day_16_input.txt"
    digits = np.array([int(d) for d in list(file.read_text())])
    offset = ('').join([str(d) for d in digits[:7]])
    orig_len = len(digits)
    s = np.sum(digits)
    digits = np.repeat(digits,10000)
    n = len(digits)
    print(n)
    pattern = [0,1,0,-1]
    m = len(pattern)
    n_iterations = 100
    for k in np.arange(n_iterations):
        old_digits = copy.deepcopy(digits)
        for i in np.arange(n):
            lims = np.arange(i,i+1,n)
            (q,r) = divmod(i+1,orig_len)
            n_tiles = ceil((n+1)/(m*(i+1)))
            coef = np.tile(np.repeat(pattern,i+1),n_tiles)[1:n+1]
            
            digits[i] = np.abs(np.dot(coef,old_digits)) % 10
        print(f"{k} FFT iterations completed")
    print(str(digits[offset:offset+8]))

if __name__ == "__main__":
    main()
