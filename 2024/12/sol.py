from pathlib import Path
from collections import deque

data_folder = Path(".").resolve()


def parse_data(data):
    garden = [list(row) for row in data.split("\n")]
    return garden


def get_candidates(point, garden, plot):
    size = (len(garden), len(garden[0]))
    curr_el = garden[point[0]][point[1]]
    cands = []
    for j in range(2):
        for d in [-1, 1]:
            cand = list(point)
            cand[j] += d
            cand = tuple(cand)
            if (
                (0 <= cand[j] < size[d])
                and (garden[cand[0]][cand[1]] == curr_el)
                and (cand not in plot)
            ):
                cands.append(cand)
    return cands


def find_garden_plot(garden, point):
    queue = deque([point])
    plot = set([point])
    while len(queue) > 0:
        point = queue.popleft()
        for candidate in get_candidates(point, garden, plot):
            queue.append(candidate)
            plot.add(candidate)
    return plot


def compute_fence_costs(garden, bulk_discount):
    processed = set()
    total_cost = 0
    for i, row in enumerate(garden):
        for j, _ in enumerate(row):
            if (i, j) in processed:
                continue
            plot = find_garden_plot(garden, (i, j))
            area = len(plot)
            perimeter = find_plot_perimeter(plot, bulk_discount)
            total_cost += area * perimeter
            processed = processed.union(plot)
    return total_cost


def find_plot_perimeter(plot, bulk_discount):
    perimeter = set()
    for point in plot:
        perimeter = perimeter.union(find_perimeter(point, plot))
    if bulk_discount:
        perimeter = merge_perimeter(perimeter)
    return len(perimeter)


def find_perimeter(point, plot):
    perimeter = set()
    for j in range(2):
        for d in [-1, 1]:
            cand = list(point)
            cand[j] += d
            cand = tuple(cand)
            if cand not in plot:
                perimeter.add((*cand, j, d))
    return perimeter


def merge_perimeter(perimeter):
    sides = list()
    processed = set()
    for fence in perimeter:
        if fence in processed:
            continue
        side = find_side(fence, perimeter)
        sides.append(side)
        processed = processed.union(side)
    return sides


def find_side(point, perimeter):
    queue = deque([point])
    side = set([point])
    while len(queue) > 0:
        point = queue.popleft()
        for candidate in find_side_neighbours(point, perimeter, side):
            queue.append(candidate)
            side.add(candidate)
    return side


def find_side_neighbours(point, perimeter, side):
    cands = []
    for d in [-1, 1]:
        cand = list(point)
        cand[1 - point[2]] += d
        cand = tuple(cand)
        if (cand in perimeter) and (cand not in side):
            cands.append(cand)
    return cands


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    garden = parse_data(data)

    print("Part 1")
    fence_cost = compute_fence_costs(garden, bulk_discount=False)
    print(f"The fence cost is {fence_cost}.")
    print()

    print("Part 2")
    fence_cost = compute_fence_costs(garden, bulk_discount=True)
    print(f"The fence cost with bulk discount is {fence_cost}.")
    print()


if __name__ == "__main__":
    main()
