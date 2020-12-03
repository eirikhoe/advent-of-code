from pathlib import Path


class map:
    def __init__(self, data):
        self.map = [list(line) for line in data.split("\n")]
        self.dim = [len(self.map), len(self.map[0])]

    def count_trees(self, slope):
        x = 0
        y = 0
        n_trees = 0
        while True:
            x = (x + slope[1]) % self.dim[1]
            y += slope[0]
            if y >= self.dim[0]:
                break
            n_trees += self.map[y][x] == "#"
        return n_trees


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    m = map(data)
    slope = (1, 3)
    tree_count = m.count_trees(slope)
    print(f"Following a slope of right {slope[1]} and down {slope[0]}")
    print(f"we encounter {tree_count} trees")
    print()

    print("Part 2")
    rem_slopes = [(1, 1), (1, 5), (1, 7), (2, 1)]
    tree_product = tree_count
    for slope in rem_slopes:
        tree_product *= m.count_trees(slope)

    print("If we multiply together the number of trees encountered on")
    print(f"each of the listed slopes we get {tree_product}")


if __name__ == "__main__":
    main()
