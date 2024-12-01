from pathlib import Path
import numpy as np
import re

data_folder = Path(".").resolve()
reg = re.compile(r"(toggle|turn on|turn off) (\d+,\d+) through (\d+,\d+)")


class Lights:
    def __init__(self, data):
        self.grid_size = (1000, 1000)
        self.grid = np.zeros(self.grid_size, dtype=int)

        self.instrs = []
        for line in data.split("\n"):
            m = reg.match(line)
            if m is None:
                raise RuntimeError()
            status = m.group(1)
            start = [int(d) for d in m.group(2).split(",")]
            end = [int(d) + 1 for d in m.group(3).split(",")]
            self.instrs.append([status, (start[1], end[1]), (start[0], end[0])])

    def follow_instructions(self):
        for instr in self.instrs:
            y = instr[1]
            x = instr[2]
            if instr[0] == "toggle":
                self.grid[y[0] : y[1], x[0] : x[1]] = (
                    1 - self.grid[y[0] : y[1], x[0] : x[1]]
                )
            elif instr[0] == "turn on":
                self.grid[y[0] : y[1], x[0] : x[1]] = 1
            else:
                self.grid[y[0] : y[1], x[0] : x[1]] = 0

    def follow_instructions_brightness(self):
        for instr in self.instrs:
            y = instr[1]
            x = instr[2]
            if instr[0] == "toggle":
                self.grid[y[0] : y[1], x[0] : x[1]] += 2
            elif instr[0] == "turn on":
                self.grid[y[0] : y[1], x[0] : x[1]] += 1
            else:
                self.grid[y[0] : y[1], x[0] : x[1]] -= 1
                self.grid[self.grid < 0] = 0

    def total_brightness(self):
        return np.sum(self.grid)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    print("Part 1")
    l = Lights(data)
    l.follow_instructions()
    print(f"{l.total_brightness()} lights are on after following the instructions")
    print()

    print("Part 2")
    l = Lights(data)
    l.follow_instructions_brightness()
    print(
        f"The total brightness is {l.total_brightness()} after following the instructions"
    )


if __name__ == "__main__":
    main()
