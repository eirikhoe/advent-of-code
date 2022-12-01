with open("input.txt", "r") as file:
    instrs = [int(instr) for instr in file.read().split(",")]


def add(ptr, instrs):
    instrs[instrs[ptr + 3]] = instrs[instrs[ptr + 1]] + instrs[instrs[ptr + 2]]
    return ptr + 4


def mult(ptr, instrs):
    instrs[instrs[ptr + 3]] = instrs[instrs[ptr + 1]] * instrs[instrs[ptr + 2]]
    return ptr + 4


def run_intcode(instrs):
    operations = {1: add, 2: mult}
    instr_ptr = 0
    while instrs[instr_ptr] is not 99:
        try:
            instr_ptr = operations[instrs[instr_ptr]](instr_ptr, instrs)
        except:
            return


found = False
for noun in range(100):
    for verb in range(100):
        mod_instrs = instrs.copy()
        mod_instrs[1] = noun
        mod_instrs[2] = verb
        run_intcode(mod_instrs)
        if mod_instrs[0] == 19690720:
            found = True
            break
    if found:
        break

print(100 * noun + verb)

