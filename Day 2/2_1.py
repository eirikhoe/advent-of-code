with open("day_2_input.txt", "r") as file:
    instrs = [int(instr) for instr in file.read().split(",")]

instrs[1] = 12
instrs[2] = 2
terminate_program = False
addr = 0
while not terminate_program:
    if instrs[addr] == 1:
        instrs[instrs[addr + 3]] = instrs[instrs[addr + 1]] + instrs[instrs[addr + 2]]
    elif instrs[addr] == 2:
        instrs[instrs[addr + 3]] = instrs[instrs[addr + 1]] * instrs[instrs[addr + 2]]
    elif instrs[addr] == 99:
        terminate_program = True
    else:
        raise RuntimeError(f"{instrs[addr]} is not a valid opcode")
    addr += 4

print(instrs[0])
