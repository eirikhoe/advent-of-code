from pathlib import Path
from numpy import argsort
import re

data_folder = Path(__file__).parent.resolve()


class Device:
    """A Class for the state of an IntCode program"""

    def __init__(self, reg=[0, 0, 0, 0]):
        self.reg = reg

    def get(self, ptr, mode):
        loc = self._find_loc(ptr, mode)
        if loc in self.instructions:
            return self.instructions[loc]
        else:
            return 0

    def set(self, ptr, mode, value):
        loc = self._find_loc(ptr, mode)
        self.instructions[loc] = value

    def _value(self, ptr, mode):
        if mode == 1:
            return ptr
        elif mode == 0:
            return self.get(ptr, 1)

    def addr(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] + self.reg[instr[1]]

    def addi(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] + instr[1]

    def mulr(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] * self.reg[instr[1]]

    def muli(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] * instr[1]

    def banr(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] & self.reg[instr[1]]

    def bani(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] & instr[1]

    def borr(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] | self.reg[instr[1]]

    def bori(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]] | instr[1]

    def setr(self, instr):
        self.reg[instr[2]] = self.reg[instr[0]]

    def seti(self, instr):
        self.reg[instr[2]] = instr[0]

    def gtir(self, instr):
        self.reg[instr[2]] = int(instr[0] > self.reg[instr[1]])

    def gtri(self, instr):
        self.reg[instr[2]] = int(self.reg[instr[0]] > instr[1])

    def gtrr(self, instr):
        self.reg[instr[2]] = int(self.reg[instr[0]] > self.reg[instr[1]])

    def eqir(self, instr):
        self.reg[instr[2]] = int(instr[0] == self.reg[instr[1]])

    def eqri(self, instr):
        self.reg[instr[2]] = int(self.reg[instr[0]] == instr[1])

    def eqrr(self, instr):
        self.reg[instr[2]] = int(self.reg[instr[0]] == self.reg[instr[1]])

    operations = {
        2: addr,
        14: addi,
        6: mulr,
        4: muli,
        7: banr,
        11: bani,
        1: borr,
        8: bori,
        12: setr,
        15: seti,
        5: gtir,
        3: gtri,
        13: gtrr,
        0: eqir,
        9: eqri,
        10: eqrr,
    }

    def operate(self, op_code, instr):
        op = Device.operations[op_code]
        op(self, instr)


file = data_folder / "input.txt"
lines = file.read_text().split("\n")

regb = re.compile(r"Before: \[(\d+), (\d+), (\d+), (\d+)\]")
reg = re.compile(r"(\d+) (\d+) (\d+) (\d+)")
rega = re.compile(r"After:  \[(\d+), (\d+), (\d+), (\d+)\]")


def main():
    before = []
    instrs = []
    after = []
    line_num = 0
    while True:
        m = regb.match(lines[line_num])
        if m is None:
            break
        before.append([int(d) for d in m.group(1, 2, 3, 4)])
        instrs.append(
            [int(d) for d in reg.match(lines[line_num + 1]).group(1, 2, 3, 4)]
        )
        after.append(
            [int(d) for d in rega.match(lines[line_num + 2]).group(1, 2, 3, 4)]
        )
        line_num += 4
    d = Device()
    n_samples = len(instrs)
    matching_three = 0
    opcodes = dict()
    for i in range(n_samples):
        possible_opcodes = set()
        for op in range(16):
            d.reg = before[i].copy()
            d.operate(op, instrs[i][1:])

            match = True
            for j, _ in enumerate(after[i]):
                if after[i][j] != d.reg[j]:
                    match = False
                    break
            if match:
                possible_opcodes.add(op)

        if instrs[i][0] not in opcodes:
            opcodes[instrs[i][0]] = possible_opcodes
        else:
            opcodes[instrs[i][0]] &= possible_opcodes

        matching_three += int(len(possible_opcodes) >= 3)

    max_len = 2

    while max_len > 1:
        for key in opcodes:
            if len(opcodes[key]) == 1:
                for key2 in opcodes:
                    if key2 != key:
                        opcodes[key2] -= opcodes[key]
        max_len = 0
        for key in opcodes:
            if len(opcodes[key]) > max_len:
                max_len = len(opcodes[key])

    print(f"There are {matching_three} samples matching three or more opcodes.\n")
    actual_code = []
    temp_code = []
    for key in opcodes:
        actual_code.append(key)
        temp_code.append(opcodes[key].pop())

    order = list(argsort(temp_code))

    print("Real opcodes corresponding to the internal ones:")
    for i in order:
        print(f"{temp_code[i]}: {actual_code[i]}")
    print()
    instrs = []
    while line_num < len(lines):
        m = reg.match(lines[line_num])
        if m:
            instrs.append([int(d) for d in m.group(1, 2, 3, 4)])
        line_num += 1

    d = Device()
    for instr in instrs:
        d.operate(instr[0], instr[1:])

    print(f"The value {d.reg[0]} is in register 0 once the program has run.")


if __name__ == "__main__":
    main()
