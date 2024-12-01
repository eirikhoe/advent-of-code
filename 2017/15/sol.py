from pathlib import Path
import numpy as np
from collections import deque
import re

data_folder = Path(".").resolve()
reg = re.compile(r"Generator (A|B) starts with (\d+)")


class Generator:
    factor = {"A": 16807, "B": 48271}
    mult_req = {"A": 4, "B": 8}

    def __init__(self, seed, gen_type, picky=False):
        self.value = seed
        self.type = gen_type
        self._picky = picky

    def generate(self):
        self.value = (self.value * Generator.factor[self.type]) % 2147483647
        if self._picky:
            while self.value % Generator.mult_req[self.type] != 0:
                self.value = (self.value * Generator.factor[self.type]) % 2147483647


class Judge:
    def __init__(self, data, picky=False):
        self.generators = dict()
        for line in data.split("\n"):
            m = reg.match(line)
            self.generators[m.group(1)] = Generator(int(m.group(2)), m.group(1), picky)
        self.count = 0

    def judge(self, n):
        names = list(self.generators.keys())
        mod_factor = 2**16
        for i in range(n):
            for name in self.generators:
                self.generators[name].generate()
            if (self.generators[names[0]].value % mod_factor) == (
                self.generators[names[1]].value % mod_factor
            ):
                self.count += 1


def main():
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    j = Judge(data)
    n = int(4e7)
    j.judge(n)

    print(f"The judge's final count after {n} values is {j.count}")
    print()

    print("Part 2")
    j = Judge(data, True)
    n = int(5e6)
    j.judge(n)

    print(f"The judge's final (picky) count after {n} values is {j.count}")
    print()


if __name__ == "__main__":
    main()
