from copy import deepcopy
from pathlib import Path
import re
from dataclasses import dataclass
import math

data_folder = Path(".").resolve()
reg = re.compile(r"(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)")


@dataclass
class Cube:
    low: list[int]
    high: list[int]

    def get_n_cubes(self):
        return math.prod([self.high[dim] + 1 - self.low[dim] for dim in range(3)])


@dataclass
class Instruction(Cube):
    on: bool


def parse_data(data):
    instructions = []
    for line in data.strip().split("\n"):
        res = reg.match(line).groups()
        on = res[0] == "on"
        coords = list(map(int, res[1:]))
        instr = Instruction(on=on, low=coords[0::2], high=coords[1::2])
        instructions.append(instr)
    return instructions


class Reactor:
    def __init__(self, instructions: list[Instruction]):
        self.cubes: list[Cube] = []
        self.instructions = instructions

    def reboot(self, limit=None):
        for instr in self.instructions:
            if (limit is None) or (max(map(abs, instr.low + instr.high)) <= limit):
                self.step(instr)

    def step(self, instr: Instruction):
        i = 0
        while i < len(self.cubes):
            cube = self.cubes[i]
            increment = False
            for dim in range(3):
                if (instr.low[dim] > cube.high[dim]) or (instr.high[dim] < cube.low[dim]):
                    increment = True
                    break
                else:
                    if cube.low[dim] < instr.low[dim]:
                        new_cube = deepcopy(cube)
                        new_cube.high[dim] = instr.low[dim] - 1
                        self.cubes[i].low[dim] = instr.low[dim]
                        self.cubes.append(new_cube)
                    if cube.high[dim] > instr.high[dim]:
                        new_cube = deepcopy(cube)
                        new_cube.low[dim] = instr.high[dim] + 1
                        self.cubes[i].high[dim] = instr.high[dim]
                        self.cubes.append(new_cube)
            if increment:
                i += 1
            else:
                self.cubes.pop(i)
        if instr.on:
            cube_data = deepcopy(instr)
            self.cubes.append(Cube(low=cube_data.low, high=cube_data.high))

    def get_total_n_cubes(self):

        return sum([cube.get_n_cubes() for cube in self.cubes])


def main():
    data = data_folder.joinpath("input.txt").read_text()
    instructions = parse_data(data)

    print("Part 1")
    r = Reactor(instructions=instructions)
    r.reboot(limit=50)
    print(r.get_total_n_cubes())
    print()

    print("Part 2")
    r = Reactor(instructions=instructions)
    r.reboot()
    print(r.get_total_n_cubes())
    print()


if __name__ == "__main__":
    main()
