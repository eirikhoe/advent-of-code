from pathlib import Path
import numpy as np
import re


def total_system_energy(positions, velocities):
    kinetic = np.sum(abs(velocities), axis=1)
    potential = np.sum(abs(positions), axis=1)
    total = np.sum(kinetic * potential)
    return total

def calculate_energy(positions,n_steps):
    velocities = np.zeros(positions.shape, dtype=int)
    change_velocities = np.zeros(positions.shape, dtype=int)
    n_planets = positions[:, 0].size
    for i in np.arange(n_steps):
        for i in np.arange(n_planets):
            other = np.full(n_planets, True)
            other[i] = False
            change_velocities[i] = np.sum(
                np.where(
                    positions[other] > positions[i],
                    1,
                    np.where(positions[other] == positions[i], 0, -1),
                ),
                axis=0,
            )
        velocities += change_velocities
        positions += velocities

    return total_system_energy(positions,velocities)

def main():
    data_folder = Path(".").resolve()
    find_coords = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    data = data_folder.joinpath("input.txt").read_text()

    positions = np.array(
        [[int(d) for d in position] for position in find_coords.findall(data)]
    )
    n_steps = 1000
    total_energy = calculate_energy(positions,n_steps)

    print(
        f"The total system energy after {n_steps} steps is {total_energy}"
    )

if __name__ == "__main__":
    main()