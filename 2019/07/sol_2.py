import itertools


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


def inp(ptr, instrs, modes, input_value):
    n_params = 1
    addr = _find_addr(ptr, instrs, modes, n_params)
    instrs[addr[0]] = input_value
    return ptr + n_params + 1


def outp(ptr, instrs, modes):
    n_params = 1
    addr = _find_addr(ptr, instrs, modes, n_params)
    return ptr + n_params + 1, instrs[addr[0]]


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


def run_intcode(instrs, input_values, instr_ptr=0):
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
    digits = [int(d) for d in str(instrs[instr_ptr])]
    k = 0
    if len(digits) == 1:
        op_mode = digits[-1]
    else:
        op_mode = digits[-2] * 10 + digits[-1]
    while op_mode is not 99:
        modes = digits[-3::-1]
        if op_mode == 3:
            instr_ptr = inp(instr_ptr, instrs, modes, input_values[k])
            k += 1
        elif op_mode == 4:
            instr_ptr, output_value = outp(instr_ptr, instrs, modes)
            return output_value, instr_ptr, op_mode
        else:
            instr_ptr = operations[op_mode](instr_ptr, instrs, modes)
        digits = [int(d) for d in str(instrs[instr_ptr])]
        if len(digits) == 1:
            op_mode = digits[-1]
        else:
            op_mode = digits[-2] * 10 + digits[-1]
    return None, None, op_mode


with open("input.txt", "r") as file:
    orig_instrs = [int(instr) for instr in file.read().split(",")]

max_signal = -int(1e20)

for perm in itertools.permutations(list(range(5, 10))):
    output_value = 0
    instrs = [0] * 5
    ptr = [0] * 5
    for i, setting in enumerate(perm):
        instrs[i] = orig_instrs.copy()
        output_value, ptr[i], op_mode = run_intcode(instrs[i], [setting, output_value])

    output = False
    while not output:
        for i in range(5):
            possible_out, ptr[i], op_mode = run_intcode(
                instrs[i], [output_value], ptr[i]
            )
            if op_mode == 99:
                output = True
                break
            else:
                output_value = possible_out
    if output_value > max_signal:
        max_signal = output_value

print(max_signal)
