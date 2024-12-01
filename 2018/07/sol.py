from pathlib import Path
import numpy as np
import re
from collections import defaultdict


def main():
    data_folder = Path(".").resolve()
    instructions = data_folder.joinpath("input.txt").read_text().split("\n")
    reg = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.")

    orders = []
    length = 0
    for instruction in instructions:
        order = reg.match(instruction)

        orders.append((ord(order.group(1)) - ord("A"), ord(order.group(2)) - ord("A")))
        for char in orders[-1]:
            if char + 1 > length:
                length = char + 1

    reqs = [[] for i in range(length)]
    inv_reqs = [[] for i in range(length)]
    todo = set()
    for order in orders:
        reqs[order[1]].append(order[0])
        inv_reqs[order[0]].append(order[1])
        todo.add(order[0])
        todo.add(order[1])

    final_order = ""
    keep_going = True
    while keep_going:
        keep_going = False
        for task, req in enumerate(reqs):
            if (not req) and (task in todo):
                final_order += chr(task + ord("A"))
                for dep_task in inv_reqs[task]:
                    reqs[dep_task].remove(task)
                todo.remove(task)
                keep_going = True
                break

    print(final_order)


if __name__ == "__main__":
    main()
