from pathlib import Path
import numpy as np
import re
from collections import defaultdict
import re

reg_str = (
    r"In state ([A-Z]):\n  If the current value is 0:\n"
    + r"    - Write the value (0|1).\n    - Move one slot to the (right|left).\n"
    + r"    - Continue with state ([A-Z]).\n  If the current value is 1:\n"
    + r"    - Write the value (0|1).\n    - Move one slot to the (right|left).\n"
    + r"    - Continue with state ([A-Z])."
)
reg = re.compile(reg_str, flags=re.MULTILINE)

reg_first = re.compile(r"Begin in state ([A-Z]).")
reg_second = re.compile(r"Perform a diagnostic checksum after (\d+) steps.")


class State:
    def __init__(self, info):
        self.values = []
        for i in range(2):
            self.values.append(
                {
                    "write_val": int(info[3 * i + 0]),
                    "dir": State.dirs[info[3 * i + 1]],
                    "next_state": info[3 * i + 2],
                }
            )


class Turing:
    dirs = {"left": -1, "right": 1}

    def __init__(self, data):
        self.on = set()
        self.loc = 0
        lines = data.split("\n")
        self.state = reg_first.match(lines[0]).group(1)
        self.checksum_number = int(reg_second.match(lines[1]).group(1))

        self.states = dict()
        states_info = reg.findall("\n".join(lines[3:]))
        for info in states_info:
            self.states[info[0]] = []
            for i in range(2):
                self.states[info[0]].append(
                    {
                        "write_val": int(info[3 * i + 1]),
                        "dir": Turing.dirs[info[3 * i + 2]],
                        "next_state": info[3 * i + 3],
                    }
                )

    def run(self, n):
        for _ in range(n):
            self.move()

    def find_checksum(self):
        self.run(self.checksum_number)
        return len(self.on)

    def move(self):
        if self.loc in self.on:
            val = 1
            if not self.states[self.state][1]["write_val"]:
                self.on.remove(self.loc)
        else:
            val = 0
            if self.states[self.state][0]["write_val"]:
                self.on.add(self.loc)
        self.loc += self.states[self.state][val]["dir"]
        self.state = self.states[self.state][val]["next_state"]

    def print_map(self):
        column_dim = [-2, 3]
        tile_columns = []
        for loc in self.on:
            if loc > column_dim[1]:
                column_dim[1] = loc
            elif loc < column_dim[0]:
                column_dim[0] = loc
            tile_columns.append(loc)

        tile_columns = np.array(tile_columns)
        map_array = np.full(
            (1, 2 * (column_dim[1] - column_dim[0]) + 3),
            4,
            dtype=int,
        )
        map_array[0, 1::2] = 0
        if tile_columns.size > 0:
            map_array[0, 2 * (tile_columns - column_dim[0]) + 1] = 1

        map_array[0, 2 * (self.loc - column_dim[0])] = 2
        map_array[0, 2 * (self.loc - column_dim[0]) + 2] = 3
        s = "\n".join(
            [
                "".join([str(d) for d in row])
                .replace("2", "[")
                .replace("3", "]")
                .replace("4", " ")
                for row in map_array
            ]
        )
        print(s)


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    t = Turing(data)
    print("Part 1")
    print(f"The diagnostic checksum of the Turing machine is {t.find_checksum()}")


if __name__ == "__main__":
    main()
