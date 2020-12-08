from pathlib import Path
from copy import deepcopy


class Console:
    """A class for the state of a console program"""

    def __init__(self, data):
        data = data.split("\n")
        self.acc = 0
        self.instr_ptr = 0
        self.instrs = []

        for line in data:
            line = line.split()
            line[-1] = int(line[-1])
            self.instrs.append(line)

    def acc(self, instr):
        self.acc += instr

    def jmp(self, instr):
        self.instr_ptr += instr - 1

    def nop(self, instr):
        pass

    operations = {
        "acc": acc,
        "jmp": jmp,
        "nop": nop,
    }

    def fix_prog(self):
        for i, instr in enumerate(self.instrs):
            instrs = deepcopy(self.instrs)
            if instr[0] == "jmp":
                instrs[i][0] = "nop"
            elif instr[0] == "nop":
                instrs[i][0] = "jmp"
            else:
                continue
            if self.run_prog(instrs):
                return (i, self.acc)

    def operate(self, op_name, instr):
        op = Console.operations[op_name]
        op(self, instr)

    def run_prog(self, instrs=None):
        if instrs is None:
            instrs = self.instrs

        self.acc = 0
        self.instr_ptr = 0
        perf_instrs = set()

        while (self.instr_ptr not in perf_instrs) and (
            0 <= self.instr_ptr < len(instrs)
        ):
            instr = instrs[self.instr_ptr]
            self.operate(instr[0], instr[1])
            perf_instrs.add(self.instr_ptr)
            self.instr_ptr += 1

        return self.instr_ptr == len(instrs)


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    console = Console(data)
    console.run_prog()
    print("Immediately before any instruction is executed a second time") 
    print(f"the value in the accumulator is {console.acc}")
    print()

    print("Part 2:")
    (i, acc) = console.fix_prog()
    print(f"After fixing the program by changing line {i} the value in") 
    print(f"the accumulator after the program terminates is {console.acc}")


if __name__ == "__main__":
    main()
