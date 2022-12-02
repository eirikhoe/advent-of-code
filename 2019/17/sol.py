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


class Camera:
    """A class for a Camera"""

    def __init__(self, prog, camera=False):
        self.map_str = ""
        self.prog = IntCodeProgram(prog)
        self.map = [[]]
        self.run()
        self.intersections = self.get_intersections()
        self.input = self.get_input()

    def get_intersections(self):
        intersections = []
        for j in range(1, len(self.map) - 1):
            for i in range(1, len(self.map[0]) - 1):
                if (
                    self.map[j][i]
                    == self.map[j - 1][i]
                    == self.map[j + 1][i]
                    == self.map[j][i + 1]
                    == self.map[j][i - 1]
                    == ord("#")
                ):
                    intersections.append([i, j])
        return intersections

    def find_sum_alignment_parameters(self):
        total = 0
        for intersection in self.intersections:
            total += intersection[0] * intersection[1]
        return total

    def wake_droid(self):
        self.prog.instructions[0] = 2

    def get_input(self):
        main = "A,A,B,C,C,A,B,C,A,B\n"
        a = "L,12,L,12,R,12\n"
        b = "L,8,L,8,R,12,L,8,L,8\n"
        c = "L,10,R,8,R,12\n"
        cam = "n\n"  # Camera not implemented
        return [ord(char) for char in list(main + a + b + c + cam)]

    def run(self):
        end_of_program = False
        input_ctr = 0
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
                    if input_ctr < len(self.input):
                        self.prog.input = self.input[input_ctr]
                        input_ctr += 1
                self.prog.operate(op_mode, modes)
                if op_mode == 4:
                    if self.prog.output < 128:
                        self.map_str += chr(self.prog.output)
                        if self.prog.output in [
                            ord(char) for char in [".", "#", "^", ">", "<", "v", "X"]
                        ]:
                            if self.map[-1]:
                                self.map[-1].append(self.prog.output)
                            else:
                                self.map[-1] = [self.prog.output]
                        elif self.prog.output == ord("\n"):
                            self.map.append([])

        while not self.map[-1]:
            self.map = self.map[:-1]
        self.prog.reset()


file = data_folder / "input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]


def main():
    print("Part 1")
    camera = Camera(instrs)
    print(camera.map_str)
    print(
        f"The sum of the alignment parameters is {camera.find_sum_alignment_parameters()}"
    )
    print()
    print("Part 2")
    camera.wake_droid()
    camera.run()
    print(f"Robot dust collected: {camera.prog.output}")


if __name__ == "__main__":
    main()
