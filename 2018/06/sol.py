from pathlib import Path
import numpy as np


def main():
    data_folder = Path(".").resolve()
    points = np.array(
        [
            [int(coord) for coord in point.split(",")]
            for point in data_folder.joinpath("input.txt").read_text().split("\n")
        ]
    )
    point_lims_x = [np.min(points[:, 0]), np.max(points[:, 0])]
    point_lims_y = [np.min(points[:, 1]), np.max(points[:, 1])]

    max_inf_area_points = 0
    n_safe_points = 0
    area = np.zeros(points.shape[0], dtype=int)

    for grid_multiplier in range(1, 20):
        grid_size_x = point_lims_x[1] - point_lims_x[0]
        grid_size_y = point_lims_y[1] - point_lims_y[0]
        grid_lims_x = [
            point_lims_x[0] - grid_size_x * grid_multiplier,
            point_lims_x[1] + grid_size_x * grid_multiplier,
        ]
        grid_lims_y = [
            point_lims_y[0] - grid_size_y * grid_multiplier,
            point_lims_y[1] + grid_size_y * grid_multiplier,
        ]
        inf_areas = set()
        min_sum_dist = 1e10
        for x_coord in np.arange(grid_lims_x[0], grid_lims_x[1]):
            top_distances = np.sum(
                np.abs(points - np.array([x_coord, grid_lims_y[0]])), axis=1
            )
            if np.sum(top_distances) < min_sum_dist:
                min_sum_dist = np.sum(top_distances)
            inf_areas.add(np.argmin(top_distances))
            bottom_distances = np.sum(
                np.abs(points - np.array([x_coord, grid_lims_y[1]])), axis=1
            )
            if np.sum(bottom_distances) < min_sum_dist:
                min_sum_dist = np.sum(bottom_distances)
            inf_areas.add(np.argmin(bottom_distances))
        for y_coord in np.arange(grid_lims_y[0], grid_lims_y[1]):
            left_distances = np.sum(
                np.abs(points - np.array([grid_lims_x[0], y_coord])), axis=1
            )
            if np.sum(left_distances) < min_sum_dist:
                min_sum_dist = np.sum(left_distances)
            inf_areas.add(np.argmin(left_distances))
            right_distances = np.sum(
                np.abs(points - np.array([grid_lims_x[1], y_coord])), axis=1
            )
            if np.sum(right_distances) < min_sum_dist:
                min_sum_dist = np.sum(right_distances)
            inf_areas.add(np.argmin(right_distances))
        if (max_inf_area_points == len(inf_areas)) and (min_sum_dist >= 10000):
            break
        elif max_inf_area_points < len(inf_areas):
            max_inf_area_points = len(inf_areas)

    print(f"Grid multiplier: {grid_multiplier}")
    for x_coord in np.arange(grid_lims_x[0], grid_lims_x[1]):
        print(x_coord)
        for y_coord in np.arange(grid_lims_y[0], grid_lims_y[1]):
            distances = np.sum(np.abs(points - np.array([x_coord, y_coord])), axis=1)
            if np.sum(distances) < 10000:
                n_safe_points += 1

            min_ind = np.argmin(distances)
            if sum(distances == distances[min_ind]) == 1:
                area[min_ind] += 1

    area[list(inf_areas)] = -1
    print("Part 1")
    print(np.argmax(area), np.max(area))
    print("Part 2")
    print(n_safe_points)


if __name__ == "__main__":
    main()
