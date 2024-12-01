from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    trees = [[int(height) for height in line] for line in data.split("\n")]
    return trees


def _is_visible(coord, trees):
    if (coord[0] in [0, len(trees) - 1]) or (coord[1] in [0, len(trees[0]) - 1]):
        return True

    x_trees = trees[coord[0]]
    y_trees = [trees[i][coord[1]] for i, _ in enumerate(trees[0])]
    tree = x_trees[coord[1]]
    obstacle = min(
        max(x_trees[: coord[1]]),
        max(x_trees[(coord[1] + 1) :]),
        max(y_trees[: coord[0]]),
        max(y_trees[(coord[0] + 1) :]),
    )
    return tree > obstacle


def count_visible(trees):
    n_visible = 0
    for y in range(len(trees)):
        for x in range(len(trees[0])):
            n_visible += _is_visible((y, x), trees)
    return n_visible


def _compute_scenic_score(coord, trees):
    if (coord[0] in [0, len(trees) - 1]) or (coord[1] in [0, len(trees[0]) - 1]):
        return 0

    x_trees = trees[coord[0]]
    y_trees = [trees[i][coord[1]] for i, _ in enumerate(trees[0])]
    rel_trees = [y_trees, x_trees]
    tree = x_trees[coord[1]]

    score = 1
    for ax in [0, 1]:
        ranges = [
            range(coord[ax] - 1, 0, -1),
            range(coord[ax] + 1, len(rel_trees[ax]) - 1),
        ]
        for d in [0, 1]:
            part_score = 0
            for i in ranges[d]:
                if rel_trees[ax][i] >= tree:
                    break
                part_score += 1
            part_score += 1
            score *= part_score
    return score


def find_maximal_scenic_score(trees):
    best_score = 0
    for y in range(len(trees)):
        for x in range(len(trees[0])):
            score = _compute_scenic_score((y, x), trees)
            if score > best_score:
                best_score = score
    return best_score


def main():
    data = data_folder.joinpath("input.txt").read_text()
    trees = parse_data(data)

    print("Part 1")
    visible_trees = count_visible(trees)
    print(f"There are {visible_trees} visible trees from outside the grid.")
    print()

    print("Part 2")
    top_scenic_score = find_maximal_scenic_score(trees)
    print(f"The top scenic score is {top_scenic_score}.")
    print()


if __name__ == "__main__":
    main()
