from pathlib import Path
import numpy as np
import copy
import time
import os
from colorama import init

init()
data_folder = Path(__file__).parent.resolve()

rg = np.random.default_rng()


class IntCodeProgram:
    """A Class for the state of an IntCode program"""

    def __init__(self, instr):
        self.instructions = dict(zip(list(range(len(instrs))), instrs))
        self._init_instructions = copy.deepcopy(self.instructions)
        self.rel_base = 0
        self.instr_ptr = 0
        self.input = None
        self.output = None

    def get(self, ptr, mode):
        loc = self._find_loc(ptr, mode)
        if loc in self.instructions:
            return self.instructions[loc]
        else:
            return 0

    def set(self, ptr, mode, value):
        loc = self._find_loc(ptr, mode)
        self.instructions[loc] = value

    def _find_loc(self, ptr, mode):
        if mode == 1:
            return ptr
        elif mode == 0:
            return self.get(ptr, 1)
        elif mode == 2:
            return self.get(ptr, 1) + self.rel_base

    def reset(self):
        self.rel_base = 0
        self.instr_ptr = 0
        self.input = None
        self.output = None
        self.instructions = copy.deepcopy(self._init_instructions)

    def add(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        self.set(
            self.instr_ptr + 2,
            modes[2],
            self.get(self.instr_ptr, modes[0]) + self.get(self.instr_ptr + 1, modes[1]),
        )
        self.instr_ptr += n_params
        return None

    def mult(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        self.set(
            self.instr_ptr + 2,
            modes[2],
            self.get(self.instr_ptr, modes[0]) * self.get(self.instr_ptr + 1, modes[1]),
        )
        self.instr_ptr += n_params

    def inp(self, modes):
        n_params = 1
        modes = modes + [0] * (n_params - len(modes))
        self.set(self.instr_ptr, modes[0], self.input)
        self.instr_ptr += n_params

    def outp(self, modes):
        n_params = 1
        modes = modes + [0] * (n_params - len(modes))
        self.output = self.get(self.instr_ptr, modes[0])
        self.instr_ptr += n_params

    def jump_if_true(self, modes):
        n_params = 2
        modes = modes + [0] * (n_params - len(modes))

        if self.get(self.instr_ptr, modes[0]) > 0:
            self.instr_ptr = self.get(self.instr_ptr + 1, modes[1])
        else:
            self.instr_ptr += n_params

    def jump_if_false(self, modes):
        n_params = 2
        modes = modes + [0] * (n_params - len(modes))

        if self.get(self.instr_ptr, modes[0]) == 0:
            self.instr_ptr = self.get(self.instr_ptr + 1, modes[1])
        else:
            self.instr_ptr += n_params

    def less_than(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        if self.get(self.instr_ptr, modes[0]) < self.get(self.instr_ptr + 1, modes[1]):
            self.set(self.instr_ptr + 2, modes[2], 1)
        else:
            self.set(self.instr_ptr + 2, modes[2], 0)
        self.instr_ptr += n_params

    def equals(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        if self.get(self.instr_ptr, modes[0]) == self.get(self.instr_ptr + 1, modes[1]):
            self.set(self.instr_ptr + 2, modes[2], 1)
        else:
            self.set(self.instr_ptr + 2, modes[2], 0)
        self.instr_ptr += n_params

    def adj_rel_base(self, modes):
        n_params = 1
        modes = modes + [0] * (n_params - len(modes))
        self.rel_base += self.get(self.instr_ptr, modes[0])
        self.instr_ptr += n_params

    operations = {
        1: add,
        2: mult,
        3: inp,
        4: outp,
        5: jump_if_true,
        6: jump_if_false,
        7: less_than,
        8: equals,
        9: adj_rel_base,
    }

    def operate(self, op_code, modes):
        op = IntCodeProgram.operations[op_code]
        return op(self, modes)


class Beam:
    def __init__(self, prog):
        self.prog = IntCodeProgram(prog)
        self.map = dict()

    def find_affected_area(self):
        area = 0
        for tile in self.map:
            area = area + self.map[tile]
        return area

    def find_closest_square(self, lim):
        distance = int(1e8)
        closest = None
        for tile in self.map:
            if (self.map[tile] == 1) and (self.map[(tile[0], tile[1] + 1)] == 0):
                current_tile = tile
                square_size = 0
                while (current_tile in self.map) and (self.map[current_tile] == 1):
                    square_size += 1
                    current_tile = (current_tile[0] + 1, current_tile[1] - 1)
                coord = (tile[0], tile[1] - square_size + 1)
                if (square_size >= lim) and ((coord[0] + coord[1]) < distance):
                    closest = coord
                    distance = coord[0] + coord[1]

        return closest

    def print_map(self):
        row_dim = [0, 0]
        column_dim = [0, 0]
        tile_rows = []
        tile_columns = []
        types = []
        for tile in self.map:
            if tile[0] > row_dim[1]:
                row_dim[1] = tile[0]
            elif tile[0] < row_dim[0]:
                row_dim[0] = tile[0]
            if tile[1] > column_dim[1]:
                column_dim[1] = tile[1]
            elif tile[1] < column_dim[0]:
                column_dim[0] = tile[1]
            tile_rows.append(tile[0])
            tile_columns.append(tile[1])
            types.append(self.map[tile])

        tile_rows = np.array(tile_rows)
        tile_columns = np.array(tile_columns)
        map_array = np.full(
            (row_dim[1] - row_dim[0] + 1, column_dim[1] - column_dim[0] + 1),
            2,
            dtype=int,
        )
        map_array[tile_rows - row_dim[0], tile_columns - column_dim[0]] = types
        path = data_folder / "map.txt"
        path.write_text(
            "\n".join(
                [
                    "".join([str(d) for d in row])
                    .replace("0", ".")
                    .replace("1", "#")
                    .replace("2", " ")
                    for row in map_array
                ]
            )
        )

    def get_map(self, area):
        for y in np.arange(area[0]):
            if (y % 100) == 0:
                print(y)
            for x in np.arange(area[1]):
                end_of_program = False
                self.prog.reset()
                curr_coord = 0
                while not end_of_program:
                    digits = [
                        int(d) for d in str(self.prog.get(self.prog.instr_ptr, 1))
                    ]
                    if len(digits) == 1:
                        op_mode = digits[-1]
                    else:
                        op_mode = digits[-2] * 10 + digits[-1]
                    if op_mode == 99:
                        end_of_program = True
                    else:
                        modes = digits[-3::-1]
                        self.prog.instr_ptr += 1
                        if op_mode == 3:
                            if curr_coord == 0:
                                self.prog.input = x
                            else:
                                self.prog.input = y
                            curr_coord = 1 - curr_coord

                        self.prog.operate(op_mode, modes)
                        if op_mode == 4:
                            self.map[(y, x)] = self.prog.output


file = data_folder / "day_19_input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]


def main():
    beam = Beam(instrs)
    beam.get_map([1200, 1200])
    beam.print_map()
    print(beam.find_affected_area())
    print(beam.find_closest_square(100))


if __name__ == "__main__":
    main()
