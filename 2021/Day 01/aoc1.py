from pathlib import Path
import numpy as np

data_folder = Path(".").resolve()


def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = [int(d) for d in data.split("\n")]

    print("Part 1")
    print(f"")
    print()

    print("Part 2")
    print(f"")
    print()


if __name__ == "__main__":
    main()
