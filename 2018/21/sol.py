from pathlib import Path
import re
from copy import deepcopy
from bisect import bisect_left
class Device:
    """A Class for the state of an IntCode program"""

    def __init__(self,data,reg = [0,0,0,0,0,0]):
        data = data.split('\n')
        self.reg = reg
        self.instr_ptr = int(re.match(r"#ip (\d)",data[0]).group(1))
        self.instrs = []
        for line in data[1:]:
            line = line.split(" ")
            for i in range(1,len(line)):
                line[i] = int(line[i])
            self.instrs.append(line) 
        self.n_instr = 0

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
        "addr": addr,
        "addi": addi,
        "mulr": mulr,
        "muli": muli,
        "banr": banr,
        "bani": bani,
        "borr": borr,
        "bori": bori,
        "setr": setr,
        "seti": seti,
        "gtir": gtir,
        "gtri": gtri,
        "gtrr": gtrr,
        "eqir": eqir,
        "eqri": eqri,
        "eqrr": eqrr,

    }

    def operate(self,op_name,instr):
        op = Device.operations[op_name]
        op(self,instr)

    def run_prog(self):
        c = 0
        while 0 <= self.reg[self.instr_ptr] < len(self.instrs):
            instr = self.instrs[self.reg[self.instr_ptr]]
            self.operate(instr[0],instr[1:])
            self.reg[self.instr_ptr] += 1
            self.n_instr += 1
            if self.reg[self.instr_ptr] == 28:
                c += 1
                print(c,[self.reg[2],self.reg[5]])

def main(): 
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    # Program is independent of register 0 until the 
    # first time we hit instruction 28. Then program exits 
    # if register 0 is equal to the current value in 
    # register 2, 8797248.

    ans = 8797248
    d = Device(data,[ans,0,0,0,0,0])
    d.run_prog()
    print(f"Program halted after {d.n_instr} instructions.")
    print(f"Register 0 had initial value {ans}.")
    print()

    print("Part 2")
    print(f"The last unique value register 2 takes is {find_last_value()}")


def find_last_value():
    x = 0
    i = 0
    vals = []
    run = True
    while run:
        y = x | 65536
        x = 4843319
        j = 0
        while y >= 256:
            if j > 0:
                y = y // 256
            x = x + (y & 255)
            x = x & 16777215
            x *= 65899
            x = x & 16777215
            j  += 1
        i += 1
        for val in vals:
            if val == x:
                return vals[-1]
        vals.append(x)

if __name__ == "__main__":
    main()
