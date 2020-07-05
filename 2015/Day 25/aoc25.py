from pathlib import Path
import re


def find_code(row, column):
    full_diagonals = row + column - 2

    full_elements = ((full_diagonals + 1) * full_diagonals) // 2

    index = full_elements + column

    value = 20151125
    for i in range(1, index):
        value = (value * 252533) % 33554393

    return value


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    reg = re.compile(
        r"To continue, please consult the code grid in the manual\."
        + r"  Enter the code at row (\d+), column (\d+)\."
    )

    row, column = (int(r) for r in reg.match(data).groups())
    code = find_code(row, column)

    print(f"The code for row {row} and column {column} is {code}")


if __name__ == "__main__":
    main()
