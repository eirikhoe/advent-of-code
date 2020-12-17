from pathlib import Path
from copy import deepcopy
from itertools import product
from collections import defaultdict


class Cubes:
    def __init__(self, data, n_dims=3):
        self.n_dims = n_dims
        self.cubes = set()
        self.adj_dirs = [
            adj
            for adj in product([1, 0, -1], repeat=n_dims)
            if ((max(adj) != 0) or (min(adj) != 0))
        ]
        cubes = [list(line) for line in data.split("\n")]
        extra_dims = [0] * (n_dims - 2)
        for row, cuberow in enumerate(cubes):
            for col, cube in enumerate(cuberow):
                if cube == "#":
                    self.cubes.add((col, row, *extra_dims))

    def evolve(self, n, show=False):
        if show:
            print("Before any cycles:\n")
            self.print_layout()
        for i in range(n):
            self.step()
            if show:
                print(f"After {i+1} cycle{'s' if i!=1 else ''}:\n")
                self.print_layout()

    def step(self):
        new_state = deepcopy(self.cubes)
        neighbours = defaultdict(lambda: 0)
        for cube in list(self.cubes):
            n_adj_on = 0
            for dir in self.adj_dirs:
                neigh_cand = [0] * self.n_dims
                for i in range(self.n_dims):
                    neigh_cand[i] = cube[i] + dir[i]
                neigh_cand = tuple(neigh_cand)
                if neigh_cand not in self.cubes:
                    neighbours[neigh_cand] += 1
                else:
                    n_adj_on += 1
            if (n_adj_on < 2) or (n_adj_on > 3):
                new_state.remove(cube)
        for neigh in neighbours:
            if neighbours[neigh] == 3:
                new_state.add(neigh)
        self.cubes = new_state

    def print_layout(self, ret=False):

        # find area
        max_lims = [None] * self.n_dims
        min_lims = [None] * self.n_dims
        for cube in list(self.cubes):
            for dim in range(self.n_dims):
                if (min_lims[dim] == None) or (cube[dim] < min_lims[dim]):
                    min_lims[dim] = cube[dim]
                if (max_lims[dim] == None) or (cube[dim] > max_lims[dim]):
                    max_lims[dim] = cube[dim]

        dims = list(zip(min_lims, max_lims))

        ranges = []
        for dim in dims[2:]:
            ranges.append(range(dim[0], dim[1] + 1))

        # make sure sorting is done first to last to match example
        ranges.reverse()
        add_coordss = []
        for r in product(*ranges):
            l = list(r)
            l.reverse()
            add_coordss.append(tuple(l))
        add_coord_names = list("zwuvrst") + [
            f"c{i}" for i in range(10, self.n_dims + 1)
        ]

        n_digits = [
            max(len(str(abs(dims[i][0]))), len(str(abs(dims[i][1]))))
            for i in range(2)
        ]
        xs = range(dims[0][0], dims[0][1] + 1)
        str_xs = [str(abs(x)).rjust(n_digits[0], " ") for x in xs]
        ys = range(dims[1][0], dims[1][1] + 1)
        str_ys = [str(abs(y)).rjust(n_digits[1], " ") for y in ys]
        x_headers = []
        for i in range(n_digits[0]):
            digits = [x[i] for x in str_xs]
            x_headers.append(" " * n_digits[1] + "".join(digits))

        line = []
        for add_coords in add_coordss:
            header_list = [
                f"{add_coord_names[i]}={c}"
                for i, c in enumerate(add_coords)
            ]
            line.append(", ".join(header_list))
            line += x_headers
            for i, y in enumerate(ys):
                s = str_ys[i]
                for x in xs:
                    coords = (x, y, *add_coords)
                    if coords in self.cubes:
                        s += "#"
                    else:
                        s += "."
                line.append(s)
            line.append("")
        output = "\n".join(line)
        if ret:
            return output
        else:
            print(output)

    def get_n_active(self):
        return len(list(self.cubes))


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()

    for info in [[1, 3], [2, 4]]:
        print(f"Part {info[0]}")
        n_dims = info[1]
        f = Cubes(data, n_dims=n_dims)
        f.evolve(6, show=False)
        n_active = f.get_n_active()
        print(f"For {n_dims} dimensions {n_active} cubes are left in ")
        print(f"the active state after the sixth cycle")
        print()


if __name__ == "__main__":
    main()
