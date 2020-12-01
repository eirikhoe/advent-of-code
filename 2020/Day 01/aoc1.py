from pathlib import Path
import numpy as np
data_folder = Path(".").resolve()

def find_factors(entries,total,n_factors):
    if n_factors == 1:
        if total in entries:
            return [total]
        else:
            return None

    for i,entry in enumerate(entries[:-1]):
        factors = find_factors(entries[i+1:],total-entry,n_factors-1)
        if factors:
            factors.append(entry)
            return factors
    return None
    


def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = [int(d) for d in data.split("\n")]
    total = 2020
    
    factors = find_factors(data,total,2)
    print("Part 1")
    print(f"The product of the two entries that sum to {total} is {np.prod(factors)}")
    print()

    factors = find_factors(data,total,3)
    print("Part 2")
    print(f"The product of the three entries that sum to {total} is {np.prod(factors)}")
    print()

if __name__ == "__main__":
    main()
