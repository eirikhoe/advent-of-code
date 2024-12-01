from pathlib import Path
import re
from copy import deepcopy
from collections import defaultdict
from bisect import bisect_left


class Device:
    """A Class for the state of an IntCode program"""

    def __init__(self, data):
        data = data.split("\n")
        self.reg = defaultdict(lambda: 0)
        self.instr_ptr = 0
        self.instrs = []
        self.played_frequency = None
        self.recovered_frequency = None
        for line in data:
            line = line.split(" ")
            for j, val in enumerate(line):
                try:
                    line[j] = int(val)
                except:
                    pass
            self.instrs.append(line)

    def snd_duet(self, instr):
        val = instr[0]
        if not isinstance(val, int):
            val = self.reg[val]
        self.played_frequency = val

    def set_duet(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] = val

    def add_duet(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] += val

    def mul_duet(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] *= val

    def mod_duet(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] = self.reg[reg_name] % val

    def rcv_duet(self, instr):
        val = instr[0]
        if not isinstance(val, int):
            val = self.reg[val]
        if val != 0:
            self.recovered_frequency = self.played_frequency

    def jgz_duet(self, instr):
        for i in range(2):
            if not isinstance(instr[i], int):
                instr[i] = self.reg[instr[i]]
        if instr[0] > 0:
            self.instr_ptr += instr[1] - 1

    operations = {
        "snd": snd_duet,
        "set": set_duet,
        "add": add_duet,
        "mul": mul_duet,
        "mod": mod_duet,
        "rcv": rcv_duet,
        "jgz": jgz_duet,
    }

    def operate(self, op_name, instr):
        op = Device.operations[op_name]
        op(self, instr)

    def run_prog(self, until_recovered=False):
        while 0 <= self.instr_ptr < len(self.instrs):
            instr = self.instrs[self.instr_ptr]
            self.operate(instr[0], instr[1:])
            self.instr_ptr += 1
            if until_recovered and (self.recovered_frequency is not None):
                break


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    d = Device(data)
    d.run_prog(True)
    print(f"The first recovered frequency is {d.recovered_frequency}")


if __name__ == "__main__":
    main()
