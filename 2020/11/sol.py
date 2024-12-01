from pathlib import Path
from copy import deepcopy


class Layout:
    def __init__(self, data, adjacent):
        self.floor = [list(line) for line in data.split("\n")]
        self.dim = [len(self.floor), len(self.floor[0])]
        self.adjacent = adjacent
        self.taken_limit = 5
        if adjacent:
            self.taken_limit = 4

    def step(self):
        new_ground = deepcopy(self.floor)
        state_change = False
        for y in range(self.dim[0]):
            for x in range(self.dim[1]):
                new_ground[y][x] = self._find_floor_type(y, x)
                if new_ground[y][x] != self.floor[y][x]:
                    state_change = True
        self.floor = new_ground
        return state_change

    def evolve_until_equilibrium(self, print_floor=False):
        if print_floor:
            print("Initial state:")
            self.print_layout()
            print()
        i = 0
        state_change = True
        while state_change:
            state_change = self.step()
            if print_floor:
                print(f"After {i+1} minute{'s' if i > 0 else ''}:")
                self.print_layout()
                print()
            i += 1

    def count_occupied(self):
        seats_taken = 0
        for y in range(self.dim[0]):
            for x in range(self.dim[1]):
                seats_taken += self.floor[y][x] == "#"
        return seats_taken

    def _find_occupied(self, y, x):
        adj_dirs = [
            [-1, -1],
            [-1, 0],
            [-1, +1],
            [0, -1],
            [0, +1],
            [+1, -1],
            [+1, 0],
            [+1, +1],
        ]
        n_occupied = 0
        for dir in adj_dirs:
            curr = [y + dir[0], x + dir[1]]
            while (0 <= curr[0] < self.dim[0]) and (0 <= curr[1] < self.dim[1]):
                n_occupied += self.floor[curr[0]][curr[1]] == "#"
                if self.adjacent or (self.floor[curr[0]][curr[1]] != "."):
                    break
                curr[0] += dir[0]
                curr[1] += dir[1]
        return n_occupied

    def _find_floor_type(self, y, x):
        occupied_count = self._find_occupied(y, x)

        if (self.floor[y][x] == "L") and (occupied_count == 0):
            return "#"
        if (self.floor[y][x] == "#") and (occupied_count >= self.taken_limit):
            return "L"

        return self.floor[y][x]

    def print_layout(self, ret=False):
        line = []
        for y in range(self.dim[0]):
            s = ""
            for k in self.floor[y]:
                s += k
            line.append(s)
        output = "\n".join(line)
        if ret:
            return output
        else:
            print(output)


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    f = Layout(data, adjacent=True)
    f.evolve_until_equilibrium()
    seats_taken = f.count_occupied()
    print(f"Checking adjacent seats {seats_taken} seats end up occupied")
    print()

    print("Part 2")
    f = Layout(data, adjacent=False)
    f.evolve_until_equilibrium()
    seats_taken = f.count_occupied()
    print(f"Checking first seat in each direction {seats_taken} seats end up occupied")


if __name__ == "__main__":
    main()
