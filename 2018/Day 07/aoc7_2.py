from pathlib import Path
import numpy as np
import re
from collections import defaultdict
from time import sleep
def main():
    data_folder = Path(".").resolve()
    instructions = data_folder.joinpath("input.txt").read_text().split("\n")
    reg = re.compile(r"Step ([A-Z]) must be finished before step ([A-Z]) can begin.")

    orders = []
    length = 0
    for instruction in instructions:
        order = reg.match(instruction)
        
        orders.append((ord(order.group(1))-ord('A'),ord(order.group(2))-ord('A')))
        for char in orders[-1]:
            if char+1 > length:
                length = char+1
    
    reqs = [[] for i in range(length)]
    inv_reqs = [[] for i in range(length)]
    todo = set()
    for order in orders:
        reqs[order[1]].append(order[0])
        inv_reqs[order[0]].append(order[1])
        todo.add(order[0])
        todo.add(order[1])

    n_workers = 5
    workers = [[-1,0] for i in range(n_workers)]
    time = 0
    min_time_left = 1
    while todo or (min_time_left > 0):
        for task,req in enumerate(reqs):
            if (not req) and (task in todo):
                for worker in workers:
                    if worker[0] == -1:
                        
                        worker[0] = task
                        worker[1] = task_time(task)
                        todo.remove(task)
                        break

        time_left = []
        for worker in workers:
            if worker[0] >= 0:
                time_left.append(worker[1])
        min_time_left = 0
        if time_left:
            min_time_left = min(time_left)
        for worker in workers:
            if worker[0] >= 0:
                worker[1] -= min_time_left
                if worker[1] == 0:
                    for dep_task in inv_reqs[worker[0]]:
                        reqs[dep_task].remove(worker[0])
                    worker[0] = -1
        time += min_time_left

    print(time)
        
def task_time(task):
    return task+61


if __name__ == "__main__":
    main()