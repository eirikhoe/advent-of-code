from pathlib import Path
import re
from copy import deepcopy
from collections import defaultdict
from bisect import bisect_left


class Device:
    """A Class for the state of an IntCode program"""

    def __init__(self, data):
        data = data.split("\n")
        self.reg = dict(zip(list("abcd"), [0] * 4))
        self.instr_ptr = 0
        self.instrs = []

        for line in data:
            line = line.split(" ")
            for j, val in enumerate(line):
                try:
                    line[j] = int(val)
                except:
                    pass
            self.instrs.append(line)

    def cpy(self, instr):
        reg_name = instr[1]
        val = instr[0]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] = val

    def inc(self, instr):
        reg_name = instr[0]
        self.reg[reg_name] += 1

    def dec(self, instr):
        reg_name = instr[0]
        self.reg[reg_name] -= 1

    def jnz(self, instr):
        for i in range(2):
            if not isinstance(instr[i], int):
                instr[i] = self.reg[instr[i]]
        if instr[0] != 0:
            self.instr_ptr += instr[1] - 1

    operations = {
        "cpy": cpy,
        "inc": inc,
        "dec": dec,
        "jnz": jnz,
    }

    def operate(self, op_name, instr):
        op = Device.operations[op_name]
        op(self, instr)

    def run_prog(self, debug=False):
        while 0 <= self.instr_ptr < len(self.instrs):
            instr = self.instrs[self.instr_ptr]
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
    print(f"Register a has the value {d.reg['a']} after running the program")
    print()

    print("Part 2:")

    d = Device(data)
    d.reg["c"] = 1
    d.run_prog()
    print(f"Register a has the value {d.reg['a']} after running the program")
    print()


if __name__ == "__main__":
    main()
