from pathlib import Path
import time

data_folder = Path(".").resolve()


class Cave:
    def __init__(self, data, floor):
        data = [
            [[int(coord) for coord in point.split(",")] for point in line.split(" -> ")]
            for line in data.split("\n")
        ]
        self.floor = floor

        self.start = (500, 0)
        self.grid = dict()
        self.grid[self.start] = "+"

        for line in data:
            for j in range(len(line) - 1):
                dim = int(line[j][0] == line[j + 1][0])
                start = min(line[j][dim], line[j + 1][dim])
                end = max(line[j][dim], line[j + 1][dim]) + 1
                c = line[j][1 - dim]
                for v in range(start, end):
                    if dim:
                        self.grid[(c, v)] = "#"
                    else:
                        self.grid[(v, c)] = "#"
        self.lowest_rock = max([p[1] for p in self.grid])

    def print_grid(self):
        s = ""
        min_col = min([p[0] for p in self.grid])
        max_col = max([p[0] for p in self.grid])
        col_size = max(abs(min_col), abs(max_col))
        min_row = min([p[1] for p in self.grid])
        max_row = self.lowest_rock + 2
        col_digits = len(str(col_size))
        row_size = max(abs(min_row), abs(max_row))
        row_digits = len(str(row_size))

        form_str = "{:" + str(col_digits) + "d}"
        for j in range(col_digits):
            s += " " * row_digits
            for loc in range(min_col, max_col + 1):
                loc_str = form_str.format(loc)
                s += loc_str[j]
            s += "\n"

        form_str = "{:" + str(row_digits) + "d}"
        for y in range(min_row, max_row):
            s += form_str.format(y)
            for x in range(min_col, max_col + 1):
                s += self.grid[(x, y)] if (x, y) in self.grid else "."
            s += "\n"
        s += form_str.format(max_row)
        for x in range(min_col, max_col + 1):
            s += "#" if self.floor else "."
        s += "\n"

        data_folder.joinpath("output.txt").write_text(s)

    def pour_grain(self):
        pos = self.start
        while (not self.floor and (pos[1] < self.lowest_rock)) or (
            self.floor and (self.grid[self.start] == "+")
        ):
            cands = [(pos[0], pos[1] + 1), (pos[0] - 1, pos[1] + 1), (pos[0] + 1, pos[1] + 1)]
            for cand in cands:
                if self.floor and (pos[1] == (self.lowest_rock + 1)):
                    continue
                if cand not in self.grid:
                    pos = cand
                    break
            else:
                self.grid[pos] = "o"
                return True
        return False

    def pour_sand(self, print):
        delay = 0.1
        if print:
            self.print_grid()
            time.sleep(delay)
        n_grains = 0
        while self.pour_grain():
            n_grains += 1
            if print:
                self.print_grid()
                time.sleep(delay)
        self.print_grid()
        return n_grains


def main():
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    cave = Cave(data, floor=False)
    n_grains = cave.pour_sand(print=False)
    print(f"{n_grains} grains of sand come to rest before flowing into the abyss.")
    print()

    print("Part 2")
    cave = Cave(data, floor=True)
    n_grains = cave.pour_sand(print=False)
    print(f"With floor {n_grains} grains of sand come to rest before blocking the source.")
    print()


if __name__ == "__main__":
    main()
