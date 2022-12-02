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


class Computer:

    n_computers = 0
    queue = []
    nat_packet = []
    sending = []
    nat_sent_y = []
    repeated_nan = False

    def __init__(self, prog):
        self.prog = IntCodeProgram(prog)
        self.has_ip = False
        self.ip = Computer.n_computers
        Computer.n_computers += 1
        Computer.queue.append([])
        Computer.sending.append([True] * 5)

    def do_instruction(self):
        end_of_program = False
        given_x = False
        output_countr = 0
        address = None
        output_package = [-1, -1]
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
                    if not self.has_ip:
                        self.prog.input = self.ip
                        self.has_ip = True
                    else:
                        if len(Computer.queue[self.ip]) == 0:
                            self.prog.input = -1
                            end_of_program = True
                        else:
                            self.prog.input = Computer.queue[self.ip].pop(0)
                            if given_x:
                                end_of_program = True
                            given_x = ~given_x
                self.prog.operate(op_mode, modes)
                if op_mode == 4:
                    if output_countr == 0:
                        address = self.prog.output
                    else:
                        output_package[output_countr - 1] = self.prog.output
                    output_countr += 1
                    if output_countr == 3:
                        if address < Computer.n_computers:
                            Computer.queue[address].append(output_package[0])
                            Computer.queue[address].append(output_package[1])
                        elif address == 255:
                            if len(Computer.nat_packet) == 0:
                                print(
                                    f"The first NAT packet has Y-value {output_package[1]}"
                                )
                            Computer.nat_packet = output_package.copy()
                        end_of_program = True
        Computer.sending[self.ip] = [*Computer.sending[self.ip][1:], op_mode == 4]

        if (
            (self.ip == (Computer.n_computers - 1))
            and (sum([sum(sending) for sending in Computer.sending]) == 0)
            and (sum([len(queue) for queue in Computer.queue]) == 0)
        ):
            if len(Computer.nat_packet) == 2:
                Computer.queue[0] = Computer.nat_packet.copy()
                if Computer.nat_packet[1] in Computer.nat_sent_y:
                    print(
                        f"The first repeated Y value sent from the NAT is {Computer.nat_packet[1]}"
                    )
                    Computer.repeated_nan = True
                Computer.nat_sent_y.append(Computer.nat_packet[1])
            for i in range(Computer.n_computers):
                Computer.sending[i] = [True] * 5


file = data_folder / "input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]


def main():
    computers = []
    for i in range(50):
        computers.append(Computer(instrs))
    while not Computer.repeated_nan:
        for i in range(50):
            computers[i].do_instruction()


if __name__ == "__main__":
    main()
