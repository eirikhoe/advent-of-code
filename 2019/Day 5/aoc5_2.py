def _find_addr(ptr, instrs, modes, n_params):
    modes = modes + [0] * (n_params - len(modes))
    addr = [0] * n_params
    for i, mode in enumerate(modes):
        if mode == 0:
            addr[i] = instrs[ptr + i + 1]
        elif mode == 1:
            addr[i] = ptr + i + 1
    return addr


def add(ptr, instrs, modes):
    n_params = 3
    addr = _find_addr(ptr, instrs, modes, n_params)
    instrs[addr[2]] = instrs[addr[0]] + instrs[addr[1]]
    return ptr + n_params + 1


def mult(ptr, instrs, modes):
    n_params = 3
    addr = _find_addr(ptr, instrs, modes, n_params)
    instrs[addr[2]] = instrs[addr[0]] * instrs[addr[1]]
    return ptr + n_params + 1


def inp(ptr, instrs, modes):
    n_params = 1
    addr = _find_addr(ptr, instrs, modes, n_params)
    instrs[addr[0]] = int(input())
    return ptr + n_params + 1


def outp(ptr, instrs, modes):
    n_params = 1
    addr = _find_addr(ptr, instrs, modes, n_params)
    print(instrs[addr[0]])
    return ptr + n_params + 1


def jump_if_true(ptr, instrs, modes):
    n_params = 2
    addr = _find_addr(ptr, instrs, modes, n_params)
    if instrs[addr[0]] > 0:
        return instrs[addr[1]]
    else:
        return ptr + n_params + 1


def jump_if_false(ptr, instrs, modes):
    n_params = 2
    addr = _find_addr(ptr, instrs, modes, n_params)
    if instrs[addr[0]] == 0:
        return instrs[addr[1]]
    else:
        return ptr + n_params + 1


def less_than(ptr, instrs, modes):
    n_params = 3
    addr = _find_addr(ptr, instrs, modes, n_params)
    if instrs[addr[0]] < instrs[addr[1]]:
        instrs[addr[2]] = 1
    else:
        instrs[addr[2]] = 0
    return ptr + n_params + 1


def equals(ptr, instrs, modes):
    n_params = 3
    addr = _find_addr(ptr, instrs, modes, n_params)
    if instrs[addr[0]] == instrs[addr[1]]:
        instrs[addr[2]] = 1
    else:
        instrs[addr[2]] = 0
    return ptr + n_params + 1


def run_intcode(instrs):
    operations = {
        1: add,
        2: mult,
        3: inp,
        4: outp,
        5: jump_if_true,
        6: jump_if_false,
        7: less_than,
        8: equals,
    }
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
