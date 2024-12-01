from pathlib import Path
from itertools import product
import re

data_folder = Path(".").resolve()
reg = re.compile(
    r"inp w\nmul x 0\nadd x z\nmod x 26\ndiv z (\d+)\nadd x (-?\d+)\n"
    + r"eql x w\neql x 0\nmul y 0\nadd y 25\nmul y x\nadd y 1\nmul z y\n"
    + r"mul y 0\nadd y w\nadd y (-?\d+)\nmul y x\nadd z y\n"
)


def analyze_prod(data):
    res = re.findall(reg, data)
    res = [[d.rjust(3) for d in r] for r in res]
    for row in res:
        print(" ".join(row))


class Device:
    """A Class for the state of an IntCode program"""

    def __init__(self, data):
        data = data.strip().split("\n")
        regs = list("wxyz")
        self.reg = dict(zip(regs, [0] * len(regs)))
        self.instrs = []
        for line in data:
            line = line.split(" ")
            for j, val in enumerate(line):
                try:
                    line[j] = int(val)
                except:
                    pass
            self.instrs.append(line)
        self.input = None

    def inp(self, instr):
        reg_name = instr[0]
        self.reg[reg_name] = self.input.pop(0)

    def add(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] += val

    def mul(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] *= val

    def sub(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] -= val

    def div(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
            if val < 0:
                raise ValueError("Negative denominator in divide")
        self.reg[reg_name] //= val

    def mod(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
            reg_val = self.reg[reg_name]
            if (val <= 0) or (reg_val < 0):
                raise ValueError("Illegal values for modulo operation")
        self.reg[reg_name] %= val

    def eql(self, instr):
        reg_name = instr[0]
        val = instr[1]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] = int(self.reg[reg_name] == val)

    operations = {
        "inp": inp,
        "add": add,
        "mul": mul,
        "sub": sub,
        "div": div,
        "mod": mod,
        "eql": eql,
    }

    def operate(self, op_name, instr):
        op = Device.operations[op_name]
        op(self, instr)

    def run_prog(self, inp, debug=False):
        for reg_name in self.reg:
            self.reg[reg_name] = 0
        self.input = inp
        for i, instr in enumerate(self.instrs):
            self.operate(instr[0], instr[1:])
            if debug:
                print(instr)
                print(self.reg)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    device = Device(data)

    # Solutions found through manual analysis using, among other things, the debug mode of run_prog
    print("Part 1")
    print(f"The largest model number accepted by monad is {99394899891971}")
    print()

    print("Part 2")
    print(f"The smallest model number accepted by monad is {92171126131911}")
    print()


if __name__ == "__main__":
    main()
