from collections import deque
import copy
from hashlib import md5
from pathlib import Path
import time

import numpy as np

data_folder = Path(__file__).parent.resolve()


def shortest_path(passcode, grid_size=4):
    initial_pos = (0, 0)
    path = ""
    queue = deque([(initial_pos, path)])
    while len(queue) > 0:
        point, path = queue.pop()
        open_choices = _find_choices(point, path, passcode)
        for candidate, direction in open_choices:
            if (min(candidate) >= 0) and (max(candidate) < grid_size):
                if candidate == (grid_size - 1, grid_size - 1):
                    return path + direction
                queue.appendleft((candidate, path + direction))
    return None


def longest_path(passcode, grid_size=4):
    initial_pos = (0, 0)
    path = ""
    queue = deque([(initial_pos, path)])
    longest_path = 0
    while len(queue) > 0:
        point, path = queue.pop()
        open_choices = _find_choices(point, path, passcode)
        for candidate, direction in open_choices:
            if (min(candidate) >= 0) and (max(candidate) < grid_size):
                if candidate == (grid_size - 1, grid_size - 1):
                    if len(path) >= longest_path:
                        longest_path = len(path) + 1
                else:
                    queue.appendleft((candidate, path + direction))

    if longest_path == 0:
        return None
    return longest_path


def _find_choices(point, path, passcode):
    candidates = [
        (point[0] - 1, point[1]),
        (point[0] + 1, point[1]),
        (point[0], point[1] - 1),
        (point[0], point[1] + 1),
    ]
    directions = ["U", "D", "L", "R"]

    hashed_string = md5(f"{passcode}{path}".encode("utf-8")).hexdigest()
    choices = list(zip(candidates, directions))
    open_choices = []
    for i in range(4):
        if int(hashed_string[i], 16) > 10:
            open_choices.append(choices[i])
    return open_choices


def main():
    passcode = "udskfozm"
    print("Part 1")
    print(f"The shortest path to reach the vault is {shortest_path(passcode)}")
    print()

    print("Part 2")
    print(f"The longest path to reach the vault is {longest_path(passcode)} steps")


if __name__ == "__main__":
    main()
