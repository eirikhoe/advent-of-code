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

        while 0 <= self.reg[self.instr_ptr] < len(self.instrs):
            instr = self.instrs[self.reg[self.instr_ptr]]
            self.operate(instr[0],instr[1:])
            self.reg[self.instr_ptr] += 1

def main(): 
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    d = Device(data)
    d.run_prog()
    print(f"The value {d.reg[0]} is in register 0 once the program has run.")
    print()

    print("Part 2:")
    # Program takes way too long to run. Answer is sum of all natural numbers n
    # for which the eventual value in register 4, 10551370, is 0 modulo n.

    number = 10551370
    reg_zero_val = 0
    for i in range(1,number+1):
        if number % i == 0:
            reg_zero_val += i
    print(f"The value {reg_zero_val} is in register 0 once the program has run.")


if __name__ == "__main__":
    main()
