from pathlib import Path
import numpy as np

data_folder = Path(".").resolve()


def parse_data(data):
    height_map = [[int(d) for d in line] for line in data.split("\n")]
    height_map = np.array(height_map, dtype=int)
    return height_map


def find_low_points(height_map):
    n_low_neighbours = np.zeros_like(height_map)
    n_low_neighbours[:-1] += (height_map[:-1] - height_map[1:]) >= 0
    n_low_neighbours[1:] += (height_map[1:] - height_map[:-1]) >= 0
    n_low_neighbours[:, :-1] += (height_map[:, :-1] - height_map[:, 1:]) >= 0
    n_low_neighbours[:, 1:] += (height_map[:, 1:] - height_map[:, :-1]) >= 0
    rows, cols = np.where(n_low_neighbours == 0)
    return tuple(rows), tuple(cols)


def compute_risk_level_sum(height_map):
    rows, cols = find_low_points(height_map)
    low_points = height_map[rows, cols]
    return np.sum(low_points + 1)


def get_basin_product(height_map):
    rows, cols = find_low_points(height_map)
    basin_sizes = np.zeros(len(rows), dtype=int)
    for i, low_point in enumerate(zip(rows, cols)):
        basin_sizes[i] = determine_basin_size(height_map, low_point)
    basin_sizes = np.sort(basin_sizes)
    return np.prod(basin_sizes[-3:])


def determine_basin_size(height_map, pos):
    map_size = height_map.shape
    explored = np.full(map_size, fill_value=False, dtype=bool)
    queue = [pos]
    explored[pos] = True
    basin_size = 1
    while len(queue) > 0:
        point = queue.pop(0)
        for candidate in _get_candidates(point, map_size):
            if (height_map[candidate] < 9) and (not explored[candidate]):
                queue.append(candidate)
                explored[candidate] = True
                basin_size += 1
    return basin_size


def _get_candidates(point, map_size):
    candidates = []
    if point[0] > 0:
        candidates.append((point[0] - 1, point[1]))
    if point[0] < map_size[0] - 1:
        candidates.append((point[0] + 1, point[1]))
    if point[1] > 0:
        candidates.append((point[0], point[1] - 1))
    if point[1] < map_size[1] - 1:
        candidates.append((point[0], point[1] + 1))
    return candidates


def main():
    data = data_folder.joinpath("input.txt").read_text()
    height_map = parse_data(data)

    print("Part 1")
    risk_level_sum = compute_risk_level_sum(height_map)
    print(
        f"The sum of the risk levels of all low points on the heightmap is {risk_level_sum}"
    )
    print()

    print("Part 2")
    basin_product = get_basin_product(height_map)
    print(f"The product of the three largest basins is {basin_product}")
    print()


if __name__ == "__main__":
    main()
