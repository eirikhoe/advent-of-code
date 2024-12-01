from collections import deque


def gen_buffer(n_steps, jump_size):
    buffer = deque([0])

    for i in range(n_steps):
        buffer.rotate(-jump_size - 1)
        buffer.appendleft(i + 1)
    return list(buffer)


def value_after_zero(n_steps, jump_size):
    zero_ind = 0
    value = None
    for i in range(n_steps):
        zero_ind = ((zero_ind - jump_size - 1) % (i + 1)) + 1
        if zero_ind == (i + 1):
            value = i + 1
    return value


def main():
    jump_size = 370
    print("Part 1")
    buffer = gen_buffer(2017, jump_size)
    print(f"The value after 2017 in the completed circular buffer is {buffer[1]}")
    print()

    print("Part 2")
    n = int(5e7)
    value = value_after_zero(n, jump_size)
    print(f"The value after 0 the moment {n} is inserted is {value}")


if __name__ == "__main__":
    main()
