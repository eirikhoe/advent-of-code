from pathlib import Path


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

    def out(self, instr):
        val = instr[0]
        if not isinstance(val, int):
            val = self.reg[val]
        print(val)

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

    operations = {
        "cpy": cpy,
        "inc": inc,
        "dec": dec,
        "jnz": jnz,
        "tgl": tgl,
        "out": out,
    }

    def operate(self):
        instr = self.instrs[self.instr_ptr]
        op_name = instr[0]
        instr = instr[1:]
        op = Device.operations[op_name]
        op(self, instr)

    def run_prog(self, debug=False):
        while 0 <= self.instr_ptr < len(self.instrs):
            self.operate()
            self.instr_ptr += 1


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    # From analyzing the code, if the intial value in register a is called a0 the code will
    # repeatedly output the binary representation of a0 + 2550 (from smallest to largest bit,
    # i.e. from right to left).
    #
    # Since the binary representation of 2550 is 100111110110 it is clear that we want a0 + 2550
    # to have the binary representation 101010101010

    d = Device(data)
    d.reg["a"] = int("101010101010", 2) - 2550
    print(
        f"The smallest positive initial value in register a that will generate the clock signal is {d.reg['a']}"
    )

    # Uncomment to verify
    # d.run_prog()


if __name__ == "__main__":
    main()
