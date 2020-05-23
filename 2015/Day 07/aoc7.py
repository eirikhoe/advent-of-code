from pathlib import Path
import numpy as np
import re

data_folder = Path(".").resolve()
reg = re.compile(r"(.*) -> (\d+|[a-z]+)")

class Circuit:

    def __init__(self,data):
        
        self.wires = dict()
        self.instrs = []

        for line in data.split('\n'):
            m = reg.match(line)
            if m is None:
                raise RuntimeError
            instr = m.group(1).split(' ')
            instr.append(m.group(2))
            if len(instr) == 2:
                op = 'ASSIGN'
            else:
                op = instr[-3]
            ordered_instr = [op]
            for i in range(len(instr)):
                if i != (len(instr)-3):
                    try:
                        instr[i] = int(instr[i])
                    except ValueError:
                        pass
                    ordered_instr.append(instr[i])
            self.instrs.append(ordered_instr)

    def reset(self):
        self.wires = dict()

    def connect(self):
        wire_not_assigned = True
        while wire_not_assigned:
            wire_not_assigned = False
            for instr in self.instrs:
                op_name = instr[0]
                args = instr[1:-1]
                wire = instr[-1]
                do_action = wire not in self.wires
                if do_action:
                    for i,_ in enumerate(args):
                        if isinstance(args[i],str):
                            if args[i] in self.wires:
                                args[i] = self.wires[args[i]]
                            else:
                                do_action = False
                                wire_not_assigned = True
                                break
                if do_action:
                    if op_name == 'ASSIGN':
                        self.wires[wire] = args[0]
                    elif op_name == 'NOT':
                        self.wires[wire] = ~args[0]
                    elif op_name == 'OR':
                        self.wires[wire] = args[0] | args[1]
                    elif op_name == 'AND':
                        self.wires[wire] = args[0] & args[1]
                    elif op_name == 'LSHIFT':
                        self.wires[wire] = args[0] << args[1]
                    elif op_name == 'RSHIFT':
                        self.wires[wire] = args[0] >> args[1]

                    self.wires[wire] = self.wires[wire] % 65536

def main():
    data = data_folder.joinpath("input.txt").read_text()
    
    print("Part 1")
    c = Circuit(data)
    c.connect()
    value = c.wires['a'] 
    print(f"Wire a ultimately has the value {value} once the circuit is connected")
    print()
    
    print("Part 2")
    c.reset()
    c.wires['b'] = value
    c.connect()
    print(f"Wire a ultimately has the value {c.wires['a']} once the circuit is connected")


if __name__ == "__main__":
    main()
