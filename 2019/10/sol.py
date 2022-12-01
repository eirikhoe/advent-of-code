from pathlib import Path

import numpy as np

data_folder = Path(".")

file = data_folder / "day_10_input.txt"
asteroids = [
    [int(d) for d in list(x)]
    for x in file.read_text().replace(".", "0").replace("#", "1").split("\n")
]
asteroids = np.array(asteroids, dtype=bool)


# Part 1

coord_y = np.tile(np.arange(asteroids.shape[0], dtype=int), (asteroids.shape[1], 1)).T
coord_x = np.tile(np.arange(asteroids.shape[1], dtype=int), (asteroids.shape[0], 1))

max_directions = 0
for i in np.arange(asteroids.shape[0], dtype=int):
    for j in np.arange(asteroids.shape[1], dtype=int):
        if asteroids[i, j]:
            other_asteroids = asteroids.copy()
            other_asteroids[i, j] = False
            dist_x = coord_x[other_asteroids] - j
            dist_y = i - coord_y[other_asteroids]
            gcd = np.gcd(dist_x, dist_y)
            directions_x = dist_x // gcd
            directions_y = dist_y // gcd
            directions = zip(directions_x, directions_y)
            unique_directions = len(set(directions))
            if unique_directions > max_directions:
                best_location = (i, j)
                max_directions = unique_directions

print(f"The best location is at {best_location[1]},{best_location[0]}.")
print(f"Here {max_directions} asteroids can be detected.")
print()

# Part 2

asteroids[best_location[0], best_location[1]] = False
n_asteroids = np.sum(asteroids, dtype=int)

coords_x = coord_x[asteroids]
coords_y = coord_y[asteroids]

dist_x = coords_x - best_location[1]
dist_y = best_location[0] - coords_y

gcd = np.gcd(dist_x, dist_y)
directions_x = dist_x // gcd
directions_y = dist_y // gcd

angle = np.pi - np.arctan2(directions_x, -directions_y)

unique_directions = list(set(zip(directions_x, directions_y)))

place = np.zeros(n_asteroids)
for unique_direction in unique_directions:
    current_asteroids = (directions_x == unique_direction[0]) & (
        directions_y == unique_direction[1]
    )
    current_size = np.sum(current_asteroids, dtype=int)
    current_ranking = np.zeros(current_size)
    current_ranking[
        np.argsort(
            np.abs(dist_x[current_asteroids]) + np.abs(dist_y[current_asteroids])
        )
    ] = np.arange(current_size)
    place[current_asteroids] = current_ranking

rank = np.zeros(n_asteroids, dtype=int)
order = np.lexsort((angle, place))
rank[order] = np.arange(n_asteroids, dtype=int)


i = 200

print(f"Asteroid {i} to be destroyed has location {coords_x[order[i-1]]},{coords_y[order[i-1]]}.")
print(f"Thus the answer to Part 2 is: {coords_x[order[i-1]] * 100 + coords_y[order[i-1]]}")

