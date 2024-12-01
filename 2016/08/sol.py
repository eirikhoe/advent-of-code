from pathlib import Path
import re
import numpy as np

data_folder = Path(".").resolve()

reg_rect = re.compile(r"rect (\d+)x(\d+)")
reg_rotate = re.compile(r"rotate (row y|column x)=(\d+) by (\d+)")


class Screen:
    def __init__(self, data):
        self.screen = np.zeros((6, 50), dtype=int)
        self.instrs = data.split("\n")

    def operate(self, i):
        instr = self.instrs[i]
        m = reg_rect.match(instr)

        if m:
            self.rectangle(int(m.group(1)), int(m.group(2)))
        else:
            m = reg_rotate.match(instr)
            if m.group(1) == "row y":
                self.rotate_row(int(m.group(2)), int(m.group(3)))
            else:
                self.rotate_column(int(m.group(2)), int(m.group(3)))

    def run(self):
        for i, _ in enumerate(self.instrs):
            self.operate(i)

    def rectangle(self, width, height):
        self.screen[:height, :width] = 1

    def rotate_row(self, index, shift):
        order = np.r_[-shift:0, 0 : self.screen.shape[1] - shift]
        self.screen[index] = self.screen[index, order]

    def rotate_column(self, index, shift):
        order = np.r_[-shift:0, 0 : self.screen.shape[0] - shift]
        self.screen[:, index] = self.screen[order, index]

    def print_screen(self):
        symbols = {0: " ", 1: "\u2588"}
        s = ""
        for i in np.arange(self.screen.shape[0]):
            for j in np.arange(self.screen.shape[1]):
                s += symbols[self.screen[i, j]]

            s += "\n"
        print(s)

    def lit_pixels(self):
        return np.sum(self.screen)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    s = Screen(data)
    s.run()

    print("Part 1")
    print(f"{s.lit_pixels()} pixels should be lit")
    print()

    print("Part 2")
    print("The screen is trying to display the code:\n")
    s.print_screen()


if __name__ == "__main__":
    main()
