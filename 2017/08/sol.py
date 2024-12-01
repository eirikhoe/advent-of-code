from pathlib import Path
import re

data_folder = Path(".").resolve()
reg = re.compile(r"(\w+) (inc|dec) (-?\d+) if (\w+) (==|!=|>=|<=|<|>) (-?\d+)")


class Instr:
    def __init__(self, mod_reg, mod, cond_reg, cond, cond_val):
        self.mod_reg = mod_reg
        self.mod = mod
        self.cond_reg = cond_reg
        self.cond = cond
        self.cond_val = cond_val


class Program:
    def __init__(self, data):
        self.registers = dict()
        self.instructions = []
        for line in data.split("\n"):
            m = reg.match(line)
            mod_reg = m.group(1)
            self.registers[mod_reg] = 0
            if m.group(2) == "inc":
                mod = int(m.group(3))
            elif m.group(2) == "dec":
                mod = -int(m.group(3))
            else:
                raise RuntimeError

            cond_reg = m.group(4)
            self.registers[cond_reg] = 0
            cond = m.group(5)
            cond_val = int(m.group(6))
            self.instructions.append(Instr(mod_reg, mod, cond_reg, cond, cond_val))

        self.all_time_max = self.max_reg()

    def run(self):
        for instr in self.instructions:
            if instr.cond == "==":
                if self.registers[instr.cond_reg] == instr.cond_val:
                    self.registers[instr.mod_reg] += instr.mod
            elif instr.cond == "!=":
                if self.registers[instr.cond_reg] != instr.cond_val:
                    self.registers[instr.mod_reg] += instr.mod
            elif instr.cond == ">=":
                if self.registers[instr.cond_reg] >= instr.cond_val:
                    self.registers[instr.mod_reg] += instr.mod
            elif instr.cond == "<=":
                if self.registers[instr.cond_reg] <= instr.cond_val:
                    self.registers[instr.mod_reg] += instr.mod
            elif instr.cond == ">":
                if self.registers[instr.cond_reg] > instr.cond_val:
                    self.registers[instr.mod_reg] += instr.mod
            elif instr.cond == "<":
                if self.registers[instr.cond_reg] < instr.cond_val:
                    self.registers[instr.mod_reg] += instr.mod
            curr_max = self.max_reg()
            if curr_max > self.all_time_max:
                self.all_time_max = curr_max

    def max_reg(self):
        max_val = None
        for reg_name in self.registers:
            reg_val = self.registers[reg_name]
            if (max_val is None) or (reg_val > max_val):
                max_val = reg_val

        return max_val


def main():
    data = data_folder.joinpath("input.txt").read_text()

    p = Program(data)
    p.run()
    print("Part 1")
    print(f"The largest register value after the program has run is {p.max_reg()}")
    print()
    print("Part 2")
    print(f"The largest register value ever seen during execution is {p.all_time_max}")


if __name__ == "__main__":
    main()
