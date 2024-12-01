from pathlib import Path
import re

data_folder = Path(".").resolve()


class Chars:
    def __init__(self, charstream):
        self.charstream = charstream
        self.score = 0
        self.garbage_amount = 0
        self.process_group(1, 1)

    def process_group(self, index, level):
        while self.charstream[index] != "}":
            if self.charstream[index] == ",":
                index += 1
            if self.charstream[index] == "<":
                index += 1
                while self.charstream[index] != ">":
                    if self.charstream[index] == "!":
                        index += 2
                    else:
                        index += 1
                        self.garbage_amount += 1
            if self.charstream[index] == "{":
                index = self.process_group(index + 1, level + 1)
            index += 1
        self.score += level
        return index


def main():
    charstream = data_folder.joinpath("input.txt").read_text()

    c = Chars(charstream)
    print("Part 1")
    print(f"The total score for all groups in the input is {c.score}")
    print()
    print("Part 2")
    print(f"There are {c.garbage_amount} non-canceled characters within the garbage")


if __name__ == "__main__":
    main()
