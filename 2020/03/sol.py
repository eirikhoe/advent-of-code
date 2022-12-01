from pathlib import Path


def count_trees(tree_map, slope):
    dim = [len(tree_map), len(tree_map[0])]
    pos = [0, 0]
    n_trees = 0
    while pos[0] < dim[0]:
        n_trees += tree_map[pos[0]][pos[1]] == "#"
        pos[1] = (pos[1] + slope[1]) % dim[1]
        pos[0] += slope[0]
    return n_trees


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    tree_map = [list(line) for line in data.split("\n")]

    print("Part 1")
    slope = (1, 3)
    tree_count = count_trees(tree_map, slope)
    print(f"Following a slope of right {slope[1]} and down {slope[0]}")
    print(f"we encounter {tree_count} trees")
    print()

    print("Part 2")
    rem_slopes = [(1, 1), (1, 5), (1, 7), (2, 1)]
    tree_product = tree_count
    for slope in rem_slopes:
        tree_product *= count_trees(tree_map, slope)

    print("If we multiply together the number of trees encountered on")
    print(f"each of the listed slopes we get {tree_product}")


if __name__ == "__main__":
    main()
