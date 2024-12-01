from pathlib import Path
import re

data_folder = Path(".").resolve()
reg = re.compile("\d+")


def list_eq(a, b):
    n = len(a)
    for i in range(n):
        if a[i] != b[i]:
            return False
    return True


def redistribute(memory):
    n = len(memory)
    max_mem = 0
    max_ind = 0
    for i in range(n):
        if memory[i] > max_mem:
            max_mem = memory[i]
            max_ind = i
    memory[max_ind] = 0
    for j in range(max_ind + 1, max_ind + max_mem + 1):
        ind = j % n
        memory[ind] += 1
    return memory


def main():
    data = data_folder.joinpath("input.txt").read_text()
    memory = [int(d) for d in reg.findall(data)]

    print("Part 1")
    duplicate = False
    seen = [memory]

    cycles = 0
    while not duplicate:
        memory = redistribute(memory.copy())
        cycles += 1
        for i in range(len(seen)):
            if list_eq(seen[i], memory):
                duplicate = True
                break
        seen.append(memory)

    print(f"It takes {cycles} cycles to reach an already seen state")
    print()

    print("Part 2")
    print(f"There are {cycles-i} cycles in the loop")
    print()


if __name__ == "__main__":
    main()
