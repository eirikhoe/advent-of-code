from pathlib import Path
import re
from copy import deepcopy
from collections import defaultdict
from bisect import bisect_left


class Programs:
    def __init__(self, data):
        instrs = []
        data = data.split("\n")
        for line in data:
            line = line.split(" ")
            for j, val in enumerate(line):
                try:
                    line[j] = int(val)
                except:
                    pass
            instrs.append(line)
        self.programs = []
        for i in range(2):
            self.programs.append(Program(instrs, i))
        self.sent_messages = [0, 0]

    def run_prog(self):
        deadlocked = False
        in_bounds = True
        while not deadlocked and in_bounds:
            for i in range(2):
                self.programs[i].step()
                if self.programs[i].sent is not None:
                    self.programs[1 - i].received.append(self.programs[i].sent)
                    self.programs[i].sent = None
                    self.sent_messages[i] += 1
            deadlocked = True
            in_bounds = False
            for i in range(2):
                deadlocked &= self.programs[i].deadlock
                in_bounds |= (
                    0 <= self.programs[i].instr_ptr < len(self.programs[i].instrs)
                )


class Program:
    def __init__(self, instrs, id):
        self.reg = defaultdict(lambda: 0)
        self.reg["p"] = id
        self.instr_ptr = 0
        self.instrs = instrs
        self.sent = None
        self.received = []
        self.deadlock = False

    def snd_duet(self, instr):
        val = instr[0]
        if not isinstance(val, int):
            val = self.reg[val]
        self.sent = val

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
        reg_name = instr[0]
        if self.received:
            self.reg[reg_name] = self.received.pop(0)
        else:
            self.instr_ptr -= 1
            self.deadlock = True

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
        op = Program.operations[op_name]
        op(self, instr)

    def step(self):
        self.deadlock = False
        if 0 <= self.instr_ptr < len(self.instrs):
            instr = self.instrs[self.instr_ptr]
            self.operate(instr[0], instr[1:])
            self.instr_ptr += 1


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 2:")
    d = Programs(data)
    d.run_prog()
    print(f"Program 1 sent {d.sent_messages[1]} messages")


if __name__ == "__main__":
    main()
