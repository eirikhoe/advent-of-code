from pathlib import Path
from copy import deepcopy


class Layout:
    def __init__(self, data):
        self.floor = [list(line) for line in data.split("\n")]
        self.dim = [len(self.floor), len(self.floor[0])]

    def _get_adj_pos(self, y, x):
        adj_coords = [
            [y - 1, x - 1],
            [y - 1, x],
            [y - 1, x + 1],
            [y, x - 1],
            [y, x + 1],
            [y + 1, x - 1],
            [y + 1, x],
            [y + 1, x + 1],
        ]
        adj_positions = []
        for coord in adj_coords:
            if (0 <= coord[0] < self.dim[0]) and (0 <= coord[1] < self.dim[1]):
                adj_positions.append(self.floor[coord[0]][coord[1]])

        return adj_positions

    def step(self, adjacent):
        new_ground = deepcopy(self.floor)
        state_change = False
        for y in range(self.dim[0]):
            for x in range(self.dim[1]):
                if adjacent:
                    new_ground[y][x] = self._find_floor_type_adj(y, x)
                else:
                    new_ground[y][x] = self._find_floor_type(y, x)
                if new_ground[y][x] != self.floor[y][x]:
                    state_change = True
        self.floor = new_ground
        return state_change

    def evolve_until_equilibrium(self, adjacent=True, print_floor=False):
        if print_floor:
            print("Initial state:")
            self.print_layout()
            print()
        i = 0
        state_change = True
        while state_change:
            state_change = self.step(adjacent)
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

    def _find_floor_type_adj(self, y, x):
        adj_positions = self._get_adj_pos(y, x)
        occupied_count = 0
        for adj_acre in adj_positions:
            occupied_count += int(adj_acre == "#")

        if (self.floor[y][x] == "L") and (occupied_count == 0):
            return "#"
        if (self.floor[y][x] == "#") and (occupied_count >= 4):
            return "L"

        return self.floor[y][x]

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
                if self.floor[curr[0]][curr[1]] == "#":
                    n_occupied += 1
                    break
                if self.floor[curr[0]][curr[1]] == "L":
                    break
                curr[0] += dir[0]
                curr[1] += dir[1]
        return n_occupied

    def _find_floor_type(self, y, x):
        occupied_count = self._find_occupied(y, x)

        if (self.floor[y][x] == "L") and (occupied_count == 0):
            return "#"
        if (self.floor[y][x] == "#") and (occupied_count >= 5):
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
    f = Layout(data)
    f.evolve_until_equilibrium(adjacent=True)
    seats_taken = f.count_occupied()
    print(f"Checking adjacent seats {seats_taken} seats end up occupied")
    print()

    print("Part 2")
    f = Layout(data)
    f.evolve_until_equilibrium(adjacent=False)
    seats_taken = f.count_occupied()
    print(f"Checking first seat in each direction {seats_taken} seats end up occupied")


if __name__ == "__main__":
    main()
