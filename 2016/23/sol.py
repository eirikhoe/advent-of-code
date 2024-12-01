from pathlib import Path
from math import factorial


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

        if isinstance(reg_name, int):
            return None

        val = instr[0]
        if not isinstance(val, int):
            val = self.reg[val]
        self.reg[reg_name] = val

    def inc(self, instr):
        reg_name = instr[0]
        if isinstance(reg_name, int):
            return None
        self.reg[reg_name] += 1

    def dec(self, instr):
        reg_name = instr[0]
        if isinstance(reg_name, int):
            return None
        self.reg[reg_name] -= 1

    def jnz(self, instr):
        for i in range(2):
            if not isinstance(instr[i], int):
                instr[i] = self.reg[instr[i]]
        if instr[0] != 0:
            self.instr_ptr += instr[1] - 1

    def tgl(self, instr):
        val = instr[0]
        if not isinstance(val, int):
            val = self.reg[val]
        ind = self.instr_ptr + val
        if 0 <= ind < len(self.instrs):
            n_args = len(self.instrs[ind][1:])
            instr_name = self.instrs[ind][0]

            if n_args == 1:
                if instr_name == "inc":
                    self.instrs[ind][0] = "dec"
                else:
                    self.instrs[ind][0] = "inc"

            if n_args == 2:
                if instr_name == "jnz":
                    self.instrs[ind][0] = "cpy"
                else:
                    self.instrs[ind][0] = "jnz"

    operations = {"cpy": cpy, "inc": inc, "dec": dec, "jnz": jnz, "tgl": tgl}

    def operate(self):
        instr = self.instrs[self.instr_ptr]
        op_name = instr[0]
        instr = instr[1:]
        op = Device.operations[op_name]
        op(self, instr)

    def run_prog(self, debug=False):
        while 0 <= self.instr_ptr < len(self.instrs):
            if debug:
                print(
                    self.instr_ptr,
                    " ".join([str(d) for d in self.instrs[self.instr_ptr]]),
                    self.reg,
                )
                input()
            self.operate()
            self.instr_ptr += 1


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    d = Device(data)
    d.reg["a"] = 7
    d.run_prog()
    print(f"The value {d.reg['a']} should be sent to the safe")
    print()

    print("Part 2:")
    # Let x be the initial value in reg a. From studying the code
    # you find it computes x! + 72*75 for x>=6.
    x = 12
    ans = factorial(x) + 72 * 75
    print(f"The value {ans} should be sent to the safe")


if __name__ == "__main__":
    main()
