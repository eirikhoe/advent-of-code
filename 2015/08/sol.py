from pathlib import Path
import numpy as np
import re

data_folder = Path(".").resolve()
reg_hex = re.compile(r"\\x[0-9a-f]{2}")
reg_qt = re.compile(r"\\\"")
reg_bslash = re.compile(r"\\\\")


def count_chars(string):
    n_code = len(string)
    n_chars = n_code

    assert (string[0] == '"') and (string[-1] == '"')
    n_chars -= 2

    n_bslash = len(reg_bslash.findall(string))
    n_chars -= n_bslash
    string = reg_bslash.sub("", string)

    n_hex = len(reg_hex.findall(string))
    n_chars -= n_hex * 3

    n_qt = len(reg_qt.findall(string))
    n_chars -= n_qt

    return n_code, n_chars


def find_decoded_diff(data):
    diff = 0
    for line in data.split("\n"):
        n_code, n_chars = count_chars(line)
        diff += n_code - n_chars
    return diff


def find_encoded_diff(data):
    diff = 0
    for line in data.split("\n"):
        diff += line.count("\\")
        diff += line.count('"')
        diff += 2
    return diff


def main():
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    output = (
        "The number of characters of code for string literals minus "
        + "the number of characters in memory for the values of the "
        + f"strings in total for the entire file is {find_decoded_diff(data)}"
    )
    print(output)
    print()

    print("Part 2")
    output = (
        "The number of characters to represent the newly encoded strings "
        + "minus the number of characters of code in each original string "
        + f"literal in total for the entire file is {find_encoded_diff(data)}"
    )
    print(output)


if __name__ == "__main__":
    main()
