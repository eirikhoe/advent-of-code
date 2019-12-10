from pathlib import Path

import numpy as np

data_folder = Path(".")

file = data_folder / "day_10_input.txt"
asteroids = [[int(d) for d in list(x)] for x in file.read_text().replace('.','0').replace('#','1').split('\n')]
asteroids = np.array(asteroids,dtype=bool)

coord_y = np.tile(np.arange(asteroids.shape[0],dtype=int), (asteroids.shape[1], 1)).T
coord_x = np.tile(np.arange(asteroids.shape[1],dtype=int), (asteroids.shape[0], 1))

max_directions = 0
for i in np.arange(asteroids.shape[0],dtype=int):
    for j in np.arange(asteroids.shape[1],dtype=int):
        if asteroids[i,j]:    
            other_asteroids = asteroids.copy()
            other_asteroids[i,j] = False
            dist_x = j-coord_x[other_asteroids]
            dist_y = i-coord_y[other_asteroids]
            gcd = np.gcd(dist_x,dist_y)
            dist_x = dist_x//gcd
            dist_y = dist_y//gcd
            directions = zip(dist_x,dist_y)
            unique_directions = len(set(directions))
            if unique_directions > max_directions:
                best_location = (j,i)
                max_directions = unique_directions

print(max_directions)
print(best_location)

