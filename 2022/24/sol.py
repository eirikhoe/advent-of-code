from pathlib import Path
from collections import deque
from copy import deepcopy
import math

data_folder = Path(".").resolve()
symb_to_vec = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}


class Maze:
    def __init__(self, data):
        lines = data.split("\n")
        n_cols = len(lines[0])
        n_rows = len(lines)
        for i in range(n_cols):
            if lines[0][i] == ".":
                self.start = (0, i)
            if lines[-1][i] == ".":
                self.end = (n_rows - 1, i)
        blizzards = {">": [], "<": [], "^": [], "v": []}
        for i in range(1, n_rows - 1):
            for j in range(1, n_cols - 1):
                if lines[i][j] in blizzards:
                    blizzards[lines[i][j]].append((i, j))
        self.initial_blizzards = blizzards
        self.size = (n_rows, n_cols)
        self.map = []
        for line in lines:
            self.map.append([])
            for char in line:
                if char == "#":
                    self.map[-1].append("#")
                else:
                    self.map[-1].append(".")
        self.period = math.lcm(n_cols - 2, n_rows - 2)

    def get_blizzards(self, time):
        blizzards = set()
        for type in self.initial_blizzards:
            dir = symb_to_vec[type]
            for pos in self.initial_blizzards[type]:
                new_pos = tuple(
                    ((pos[i] - 1 + dir[i] * time) % (self.size[i] - 2)) + 1 for i in range(2)
                )
                blizzards.add(new_pos)
        return blizzards

    def solve(self, n_times):
        time = self._solve_one_way(self.start, self.end, 0)
        for _ in range(n_times - 1):
            time = self._solve_one_way(self.end, self.start, time)
            time = self._solve_one_way(self.start, self.end, time)
        return time

    def _solve_one_way(self, start, end, init_time):
        forward = (end[0] - start[0]) > 0
        initial = (start, init_time)
        candidates = [initial]
        best = None
        seen = dict()

        blizzards = deepcopy(self.initial_blizzards)
        while len(candidates) > 0:
            curr = candidates.pop()
            if curr[0] == end:
                if (best is None) or (curr[1] < best):
                    best = curr[1]
            if (best is not None) and (curr[1] >= best):
                continue
            time = curr[1] + 1
            blizzards = self.get_blizzards(time)
            cands_before_blizzards = self.get_candidates(curr[0], forward)
            cands = []
            for cand in cands_before_blizzards:
                if cand not in blizzards:
                    cands.append(cand)
            for cand in cands:
                seen_cand = (cand[0], cand[1], time % self.period)
                periods = time // self.period
                if (seen_cand not in seen) or (periods < seen[seen_cand]):
                    candidates.append((cand, time))
                    seen[seen_cand] = periods
        return best

    def get_candidates(self, pos, forward):
        candidates = []
        if forward:
            order = [-1, 1]
        else:
            order = [1, -1]
        for j in order:
            for i in range(2):
                cand = list(pos)
                cand[i] += j
                if (
                    (0 <= cand[0] < self.size[0])
                    and (0 <= cand[1] < self.size[1])
                    and (self.map[cand[0]][cand[1]] == ".")
                ):
                    candidates.append(tuple(cand))
            if j == order[0]:
                candidates.append(pos)
        return candidates


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    maze = Maze(data)

    print("Part 1")
    time = maze.solve(1)
    print(f"The fewest minutes required to reach the goal is {time}.")
    print()

    print("Part 2")
    time = maze.solve(2)
    print(f"The fewest minutes required to reach the goal twice is {time}.")
    print()


if __name__ == "__main__":
    main()
