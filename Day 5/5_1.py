


def add(ptr, instrs, modes):
    ptr +=1
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    addr = [0] * n_params
    for i, mode in enumerate(modes):
        if mode == 0:
            addr[i] = instrs[ptr + i]
        elif mode == 1:
            addr[i] = ptr + i
    instrs[addr[2]] = instrs[addr[0]] + instrs[addr[1]]
    return ptr + n_params

def mult(ptr, instrs, modes):
    ptr +=1
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    addr = [0] * n_params
    for i, mode in enumerate(modes):
        if mode == 0:
            addr[i] = instrs[ptr + i]
        elif mode == 1:
            addr[i] = ptr + i
    instrs[addr[2]] = instrs[addr[0]] * instrs[addr[1]]
    
    return ptr + n_params

def inp(ptr, instrs,modes):
    ptr +=1
    n_params = 1
    modes = modes + [0] * (n_params - len(modes))
    addr = [0] * n_params
    for i, mode in enumerate(modes):
        if mode == 0:
            addr[i] = instrs[ptr + i]
        elif mode == 1:
            addr[i] = ptr + i

    instrs[addr[0]] = int(input())
    return ptr + n_params
    
def outp(ptr, instrs,modes):
    ptr +=1
    n_params = 1
    modes = modes + [0]*(n_params - len(modes))
    addr = [0] * n_params
    for i, mode in enumerate(modes):
        if mode == 0:
            addr[i] = instrs[ptr + i]
        elif mode == 1:
            addr[i] = ptr + i

    print(instrs[addr[0]])
    return ptr + n_params




def run_intcode(instrs):
    operations = {1: add, 2: mult, 3: inp, 4: outp}
    instr_ptr = 0
    digits = [int(d) for d in str(instrs[instr_ptr])]
    if len(digits) == 1:
        op_mode = digits[-1]
    else:
        op_mode = digits[-2] * 10 + digits[-1]
    while op_mode is not 99:        
        modes = digits[-3::-1]
        instr_ptr = operations[op_mode](instr_ptr, instrs, modes)
        digits = [int(d) for d in str(instrs[instr_ptr])]
        if len(digits) == 1:
            op_mode = digits[-1]
        else:
            op_mode = digits[-2] * 10 + digits[-1]
    
with open("day_5_input.txt", "r") as file:
    instrs = [int(instr) for instr in file.read().split(",")]

run_intcode(instrs)
