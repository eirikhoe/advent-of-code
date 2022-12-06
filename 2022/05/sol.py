from pathlib import Path
import re
from copy import deepcopy

data_folder = Path(".").resolve()

def parse_data(data):
    instr_parse = re.compile(r"move (\d+) from (\d+) to (\d+)")
    lines = data.split("\n")
    max_height = 0
    while "[" in lines[max_height]:
        max_height += 1
    n_stacks = int(lines[max_height].split()[-1])
    instrs = []
    for i in range(max_height+2,len(lines)):
        g = instr_parse.match(lines[i]).groups()
        instr = [int(loc)-1 for loc in g]
        instr[0] = instr[0]+1
        instrs.append(tuple(instr))
    stacks = [[] for i in range(n_stacks)]
    for i in range(max_height-1,-1,-1):
        for j in range(n_stacks):
            char =  lines[i][1+4*j]
            if char == " ":
                continue
            else:
                stacks[j].append(char)

    return stacks, instrs

def move(stacks,instrs,type):
    stacks = deepcopy(stacks)
    for instr in instrs:
        if type == "old":
            for _ in range(instr[0]):
                stacks[instr[2]].append(stacks[instr[1]].pop())
        else:
            n = instr[0]
            moved = stacks[instr[1]][-n:]
            stacks[instr[1]] = stacks[instr[1]][:-n]
            stacks[instr[2]].extend(moved)
    message = [stack[-1] for stack in stacks]
    message = "".join(message)
    return message
    

def main():
    data = data_folder.joinpath("input.txt").read_text()
    stacks, instrs = parse_data(data)

    print("Part 1")
    message = move(stacks,instrs,type="old")
    print(f"For the Cratemover 9000 the top crates spell the message {message}")
    print()

    print("Part 2")
    message = move(stacks,instrs,type="new")
    print(f"For the Cratemover 9001 the top crates spell the message {message}")
    print()


if __name__ == "__main__":
    main()
