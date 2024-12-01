from pathlib import Path
import re
from copy import deepcopy
from collections import defaultdict
from bisect import bisect_left


class Device:
    """A Class for the state of an IntCode program"""

    def __init__(self, data):
        data = data.split("\n")
        self.reg = dict(zip(list("abcdefgh"), [0] * 8))
        self.instr_ptr = 0
        self.instrs = []
        self.count_mul = 0

        for line in data:
            line = line.split(" ")
            for j, val in enumerate(line):
                try:
                    line[j] = int(val)
                except:
                    pass
            self.instrs.append(line)

    def set_duet(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] = val

    def sub_duet(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] -= val

    def mul_duet(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] *= val

    def jnz_duet(self, instr):
        for i in range(2):
            if not isinstance(instr[i], int):
                instr[i] = self.reg[instr[i]]
        if instr[0] != 0:
            self.instr_ptr += instr[1] - 1

    operations = {
        "sub": sub_duet,
        "set": set_duet,
        "mul": mul_duet,
        "jnz": jnz_duet,
    }

    def operate(self, op_name, instr):
        op = Device.operations[op_name]
        op(self, instr)

    def run_prog(self, debug=False):
        while 0 <= self.instr_ptr < len(self.instrs):
            instr = self.instrs[self.instr_ptr]
            if instr[0] == "mul":
                self.count_mul += 1

            if debug:
                print(self.instr_ptr)
                print(instr)
                print(self.reg)
                input()

            self.operate(instr[0], instr[1:])
            self.instr_ptr += 1


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    d = Device(data)
    d.run_prog()
    print(f"The mul instruction is invoked {d.count_mul} times")
    print()

    print("Part 2:")
    # The final value in registry h will be the number of non prime number in the set
    # {106500,106517,106534,....,123500}. The end points are the values in the registers
    # b and c respectively after the program has done the initial set up (instruction 7).
    n_non_primes = find_non_primes(106500, 123500, 17)
    print(
        f"The value left in register h if the program was run to completion would be {n_non_primes}"
    )


def find_non_primes(start, end, jump):
    n_non_primes = 0
    for number in range(start, end + 1, jump):
        for j in range(2, number):
            if number % j == 0:
                n_non_primes += 1
                break
    return n_non_primes


if __name__ == "__main__":
    main()
