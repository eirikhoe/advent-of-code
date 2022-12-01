from pathlib import Path


class Device:
    """A Class for the state of an IntCode program"""

    def __init__(self, data):
        data = data.split("\n")
        reg_names = "ab"
        self.reg = dict(zip(list(reg_names), [0] * len(reg_names)))
        self.instr_ptr = 0
        self.instrs = []

        for line in data:
            line = line.split(" ")
            for j, val in enumerate(line):
                line[j] = line[j].rstrip(",")
                try:
                    line[j] = int(val)
                except ValueError:
                    pass
            self.instrs.append(line)

    def inc(self, instr):
        reg_name = instr[0]
        self.reg[reg_name] += 1

    def tpl(self, instr):
        reg_name = instr[0]
        self.reg[reg_name] *= 3

    def hlf(self, instr):
        reg_name = instr[0]
        self.reg[reg_name] /= 2

    def jmp(self, instr):
        jmp_size = instr[0]
        self.instr_ptr += jmp_size - 1

    def jie(self, instr):
        reg_name = instr[0]
        reg_value = self.reg[reg_name]
        jmp_size = instr[1]
        if (reg_value % 2) == 0:
            self.instr_ptr += jmp_size - 1

    def jio(self, instr):
        reg_name = instr[0]
        reg_value = self.reg[reg_name]
        jmp_size = instr[1]
        if reg_value == 1:
            self.instr_ptr += jmp_size - 1

    operations = {
        "hlf": hlf,
        "tpl": tpl,
        "inc": inc,
        "jmp": jmp,
        "jie": jie,
        "jio": jio,
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
    print(
        f"Register b has the value {d.reg['b']} after running the "
        + "program with starting register values a=0, b=0"
    )
    print()

    print("Part 2:")
    d = Device(data)
    d.reg["a"] = 1
    d.run_prog()
    print(
        f"Register b has the value {d.reg['b']} after running the "
        + "program with starting register values a=1, b=0"
    )
    print()


if __name__ == "__main__":
    main()
