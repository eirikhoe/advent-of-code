from pathlib import Path
import numpy as np
import re
from collections import defaultdict

mask_re = re.compile(r"mask = ([X01]{36})")
mem_re = re.compile(r"mem\[(\d+)\] = (\d+)")

def _make_binary(dec_int, length):
    return list(bin(dec_int)[2:].rjust(length, "0"))

class BitMask:
    """A class for the state of a bitmask program"""

        
    def __init__(self, data):
        self.memory = defaultdict(lambda: 0)
        data = data.split("\n")
        self.instrs = []
        for line in data:
            g = mask_re.match(line)
            if g is not None:
                g = g.groups()
                self.instrs.append(["mask", np.array(list(g[0]))])
            else:
                g = mem_re.match(line).groups()
                self.instrs.append(["mem", [int(g[0]), int(g[1])]])
        self.n_bits = 36
        self.curr_mask = np.array(["X"] * self.n_bits)

    def run_program(self, version=1):
        for instr in self.instrs:
            if instr[0] == "mask":
                self.curr_mask = instr[1]
                continue
            if version == 1:
                self.write_to_mem(instr[1])
            elif version == 2:
                self.write_to_mem_v2(instr[1])

    def write_to_mem(self, instr):
        value = _make_binary(instr[1], self.n_bits)
        value = np.where(self.curr_mask != "X", self.curr_mask, value)
        dec_value = int("".join(value), 2)
        self.memory[instr[0]] = dec_value

    def write_to_mem_v2(self, instr):
        value = _make_binary(instr[0], self.n_bits)
        value = np.where(self.curr_mask != "0", self.curr_mask, value)

        floating_indicies = np.arange(self.n_bits)[value == "X"]
        n_floating_bits = len(floating_indicies)
        for i in range(2 ** n_floating_bits):
            rep_bits = _make_binary(i, n_floating_bits)
            value[floating_indicies] = rep_bits
            dec_value = int("".join(value), 2)
            self.memory[dec_value] = instr[1]

    def sum_memory(self):
        total = 0
        for loc in self.memory:
            total += self.memory[loc]
        return total


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    prog = BitMask(data)
    prog.run_program()
    print(f"The sum of all values left in memory is {prog.sum_memory()}")
    print()

    print("Part 2")
    prog = BitMask(data)
    prog.run_program(version=2)
    print(
        f"The sum of all values left in memory for version 2 is {prog.sum_memory()}"
    )


if __name__ == "__main__":
    main()
