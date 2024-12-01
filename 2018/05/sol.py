from pathlib import Path
import numpy as np
import re
from time import perf_counter


def react_polymer(polymer):
    polymer = polymer.copy()
    completed = False
    while not completed:
        completed = True
        for i in range(len(polymer) - 1):
            if abs(ord(polymer[i]) - ord(polymer[i + 1])) == 32:
                del polymer[i : i + 2]
                completed = False
                break
    return polymer


def reduce_polymer(polymer, unit):
    reduced_polymer = list(
        filter(lambda a: (a != unit.upper()) and (a != unit.lower()), polymer)
    )
    return reduced_polymer


def main():
    data_folder = Path(".").resolve()
    polymer = data_folder.joinpath("input.txt").read_text()
    polymer = list(polymer)

    reacted_polymer = react_polymer(polymer)

    print(f"The reacted polymer has length {len(reacted_polymer)}.")

    min_length = len(polymer) + 1
    for code_point in range(65, 65 + 26):
        unit = chr(code_point)
        reduced_polymer = reduce_polymer(polymer, unit)
        reacted_reduced_length = len(react_polymer(reduced_polymer))
        if reacted_reduced_length < min_length:
            min_length = reacted_reduced_length
            best_unit_int = code_point

        print(f"{unit}: Length {reacted_reduced_length}")

    print(f"The best unit to remove was {chr(best_unit_int)}/{chr(best_unit_int+32)}.")
    print(f"This gave a reduced polymer with length {min_length} after reaction.")


if __name__ == "__main__":
    main()
