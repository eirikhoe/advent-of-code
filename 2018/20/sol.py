from pathlib import Path
import numpy as np


def _get_candidates(point):
    return [
        (point[0] - 1, point[1]),
        (point[0], point[1] - 1),
        (point[0], point[1] + 1),
        (point[0] + 1, point[1]),
    ]


class Regex:
    move = {"E": (0, 1), "W": (0, -1), "N": (-1, 0), "S": (1, 0)}
    door = {"E": "|", "W": "|", "N": "-", "S": "-"}

    def __init__(self, reg):
        self.reg = reg[1:-1]
        self.map = {(0, 0): "X"}
        self.draw_map()
        self.lims = [[0, 0], [0, 0]]
        for loc in self.map:
            if loc[0] < self.lims[0][0]:
                self.lims[0][0] = loc[0]
            if loc[0] > self.lims[0][1]:
                self.lims[0][1] = loc[0]
            if loc[1] < self.lims[1][0]:
                self.lims[1][0] = loc[1]
            if loc[1] > self.lims[1][1]:
                self.lims[1][1] = loc[1]
        self.lims[0][0] -= 1
        self.lims[0][1] += 1
        self.lims[1][0] -= 1
        self.lims[1][1] += 1
        self.size = (
            self.lims[0][1] - self.lims[0][0] + 1,
            self.lims[1][1] - self.lims[1][0] + 1,
        )
        self.grid = []
        for y in range(self.size[0]):
            self.grid.append([])
            for x in range(self.size[1]):
                loc = (y + self.lims[0][0], x + self.lims[1][0])
                if loc in self.map:
                    self.grid[y].append(self.map[loc])
                else:
                    self.grid[y].append("#")

    def draw(self, regex, loc):
        i = 0

        while i < len(regex):
            if regex[i] in ["E", "W", "N", "S"]:
                v = Regex.move[regex[i]]
                self.map[(loc[0] + v[0], loc[1] + v[1])] = Regex.door[regex[i]]
                loc = loc[0] + 2 * v[0], loc[1] + 2 * v[1]
                self.map[loc] = "."
                i += 1
            elif regex[i] == "(":
                children, j = Regex.children(regex[i:])
                i += j
                child_locs = []
                for child in children:
                    child_locs.append(self.draw(child, loc))
                same_end = True
                for j in range(1, len(child_locs)):
                    if child_locs[j] != child_locs[0]:
                        same_end = False
                if (not same_end) and (i < len(regex)):
                    raise RuntimeError("Child paths ended in different locations")
                else:
                    loc = child_locs[0]
        return loc

    def print_map(self):
        s = []
        for y, row in enumerate(self.grid):
            r = "".join(row)
            s.append(r)
        print("\n".join(s))

    @staticmethod
    def children(route):
        level = 1
        children = []
        child = ""
        j = 1
        while True:
            if route[j] == "(":
                level += 1
            elif route[j] == ")":
                level -= 1
                if level == 0:
                    children.append(child)
                    break

            if (level == 1) and route[j] == "|":
                children.append(child)
                child = ""
            else:
                child += route[j]
            j += 1
        return children, j + 1

    def draw_map(self):
        self.draw(self.reg, (0, 0))

    def bfs(self, pos):
        n_doors = np.full(self.size, -1, dtype=int)
        n_doors[pos] = 0
        queue = [pos]
        while len(queue) > 0:
            point = queue.pop(0)
            for candidate in _get_candidates(point):
                if (n_doors[candidate] < 0) and (
                    self.grid[candidate[0]][candidate[1]] != "#"
                ):
                    if self.grid[candidate[0]][candidate[1]] in ["|", "-"]:
                        n_doors[candidate] = n_doors[point] + 1
                    else:
                        n_doors[candidate] = n_doors[point]
                    queue.append(candidate)
        return n_doors

    def max_doors(self):
        n_doors = self.bfs((0 - self.lims[0][0], 0 - self.lims[1][0]))
        return np.max(n_doors)

    def rooms_enough_away(self, n):
        n_doors = self.bfs((0 - self.lims[0][0], 0 - self.lims[1][0]))
        valid_rooms = 0
        for y in range(self.size[0]):
            for x in range(self.size[1]):
                if (self.grid[y][x] == ".") and (n_doors[(y, x)] >= n):
                    valid_rooms += 1
        return valid_rooms


def main():
    data_folder = Path(".").resolve()
    text = data_folder.joinpath("input.txt").read_text()

    print("Part 1:")
    r = Regex(text)
    print(f"Furthest room requires passing {r.max_doors()} doors")
    # r.print_map()
    print()

    print("Part 2:")
    n = 1000
    print(
        f"There are {r.rooms_enough_away(n)} rooms that require passing at least {n} doors"
    )


if __name__ == "__main__":
    main()
