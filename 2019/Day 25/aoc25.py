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


class Droid:
    def __init__(self, prog):
        self.prog = IntCodeProgram(prog)
        self.input = []
        self.output = ""

    def run(self):
        end_of_program = False
        self.prog.input = 1
        while not end_of_program:
            digits = [int(d) for d in str(self.prog.get(self.prog.instr_ptr, 1))]
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
                    if len(self.input) == 0:
                        self.input = list(input() + "\n")
                    self.prog.input = ord(self.input.pop(0))

                self.prog.operate(op_mode, modes)
                if op_mode == 4:
                    self.output += chr(self.prog.output)
                    if self.output[-9:] == "Command?\n":
                        print(self.output)
                        self.output = ""
        print(self.output)


file = data_folder / "day_25_input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]


def main():
    droid = Droid(instrs)
    droid.run()


if __name__ == "__main__":
    main()
