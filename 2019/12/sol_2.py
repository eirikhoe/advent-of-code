from math import gcd
from pathlib import Path
import re

import numpy as np


def find_duplicate_state_1d(coords):
    velocities = np.zeros(coords.shape, dtype=int)
    change_velocities = np.zeros(coords.shape, dtype=int)
    initial_state = np.concatenate([coords, velocities], axis=1)
    duplicate_state_found = False
    n_steps = 0
    n_planets = coords.size
    while not duplicate_state_found:
        for i in np.arange(coords.shape[0]):
            other = np.full(n_planets, True)
            other[i] = False
            change_velocities[i] = np.sum(
                np.where(
                    coords[other] > coords[i],
                    1,
                    np.where(coords[other] == coords[i], 0, -1),
                ),
                axis=0,
            )
        velocities += change_velocities
        coords += velocities
        n_steps += 1
        current_state = np.concatenate([coords, velocities], axis=1)
        if np.array_equal(initial_state, current_state):
            duplicate_state_found = True

    return n_steps


def steps_to_duplicate(loop_sizes):
    steps = loop_sizes[0]
    for i in range(1, len(loop_sizes)):
        steps = steps * loop_sizes[i] // gcd(steps, loop_sizes[i])
    return steps


def main():
    data_folder = Path(".").resolve()
    find_coords = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    data = data_folder.joinpath("input.txt").read_text()
    positions = np.array(
        [[int(d) for d in position] for position in find_coords.findall(data)]
    )

    n_dimensions = positions[0].size
    dim_dict = {0: "x", 1: "y", 2: "z"}
    steps_dim = [0] * n_dimensions

    for dim in np.arange(n_dimensions):
        coords = positions[:, dim : dim + 1]
        steps_dim[dim] = find_duplicate_state_1d(coords)
        print(
            f"Result just for {dim_dict[dim]}: {steps_dim[dim]} steps to reach a duplicate state.\n"
        )

    print(
        f"It takes a total of {steps_to_duplicate(steps_dim)} steps to reach a duplicate universe state."
    )


if __name__ == "__main__":
    main()
