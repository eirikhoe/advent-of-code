from pathlib import Path

data_folder = Path("C:/Users/Eirik/Documents/Python Scripts/Advent of Code/Day 9")


class IntCodeProgram:
    """A Class for the state of an IntCode program"""

    def __init__(self, instr):
        self.instructions = dict(zip(list(range(len(instrs))), instrs))
        self.rel_base = 0
        self.instr_ptr = 0

    def get(self, ptr, mode):
        loc = self._find_loc(ptr, mode)
        if loc in self.instructions:
            return self.instructions[loc]
        else:
            return 0

    def set(self, ptr, value, mode):
        loc = self._find_loc(ptr, mode)
        self.instructions[loc] = value

    def _find_loc(self, ptr, mode):
        if mode == 1:
            return ptr
        elif mode == 0:
            return self.get(ptr, 1)
        elif mode == 2:
            return self.get(ptr, 1) + self.rel_base


def add(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    prog.set(
        prog.instr_ptr + 2,
        prog.get(prog.instr_ptr, modes[0]) + prog.get(prog.instr_ptr + 1, modes[1]),
        modes[2],
    )
    prog.instr_ptr += n_params


def mult(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    prog.set(
        prog.instr_ptr + 2,
        prog.get(prog.instr_ptr, modes[0]) * prog.get(prog.instr_ptr + 1, modes[1]),
        modes[2],
    )
    prog.instr_ptr += n_params


def inp(prog, modes):
    n_params = 1
    modes = modes + [0] * (n_params - len(modes))
    prog.set(prog.instr_ptr, int(input()), modes[0])
    prog.instr_ptr += n_params


def outp(prog, modes):
    n_params = 1
    modes = modes + [0] * (n_params - len(modes))
    print(prog.get(prog.instr_ptr, modes[0]))
    prog.instr_ptr += n_params


def jump_if_true(prog, modes):
    n_params = 2
    modes = modes + [0] * (n_params - len(modes))

    if prog.get(prog.instr_ptr, modes[0]) > 0:
        prog.instr_ptr = prog.get(prog.instr_ptr + 1, modes[1])
    else:
        prog.instr_ptr += n_params


def jump_if_false(prog, modes):
    n_params = 2
    modes = modes + [0] * (n_params - len(modes))

    if prog.get(prog.instr_ptr, modes[0]) == 0:
        prog.instr_ptr = prog.get(prog.instr_ptr + 1, modes[1])
    else:
        prog.instr_ptr += n_params


def less_than(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    if prog.get(prog.instr_ptr, modes[0]) < prog.get(prog.instr_ptr + 1, modes[1]):
        prog.set(prog.instr_ptr + 2, 1, modes[2])
    else:
        prog.set(prog.instr_ptr + 2, 0, modes[2])
    prog.instr_ptr += n_params


def equals(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    if prog.get(prog.instr_ptr, modes[0]) == prog.get(prog.instr_ptr + 1, modes[1]):
        prog.set(prog.instr_ptr + 2, 1, modes[2])
    else:
        prog.set(prog.instr_ptr + 2, 0, modes[2])
    prog.instr_ptr += n_params


def adj_rel_base(prog, modes):
    n_params = 1
    modes = modes + [0] * (n_params - len(modes))
    prog.rel_base += prog.get(prog.instr_ptr, modes[0])
    prog.instr_ptr += n_params


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


def perform_instruction(prog):
    digits = [int(d) for d in str(prog.get(prog.instr_ptr, 1))]
    if len(digits) == 1:
        op_mode = digits[-1]
    else:
        op_mode = digits[-2] * 10 + digits[-1]
    if op_mode == 99:
        return True
    else:
        modes = digits[-3::-1]
        prog.instr_ptr += 1
        operations[op_mode](prog, modes)
        return False


def run_intcode(prog):

    end_of_program = False
    while not end_of_program:
        end_of_program = perform_instruction(prog)


file = data_folder / "day_9_input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]


prog = IntCodeProgram(instrs)
run_intcode(prog)
