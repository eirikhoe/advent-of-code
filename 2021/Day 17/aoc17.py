from pathlib import Path
import numpy as np
import parse

data_folder = Path(".").resolve()


def parse_data(data):
    reg = parse.compile("target area: x={}..{}, y={}..{}")
    v = reg.parse(data).fixed
    x_target = sorted(list(map(int, [v[0], v[1]])))
    y_target = sorted(list(map(int, [v[2], v[3]])))
    return x_target, y_target


def find_quantities(x_target, y_target):
    assert x_target[0] > 0
    assert y_target[1] < 0
    x_low = int(np.sqrt(x_target[0]))
    x_high = x_target[1]
    y_low = y_target[0]
    y_high = -y_target[0]
    max_high_y = 0
    n_valid_trajectories = 0
    for v_x in range(x_low, x_high + 1):
        for v_y in range(y_low, y_high + 1):
            trajectory = sim_trajectory(v_x, v_y, x_target, y_target)
            if trajectory is not None:
                n_valid_trajectories += 1
                high_y = trajectory[max(v_y, 0)][1]
                if max_high_y < high_y:
                    max_high_y = high_y
    return n_valid_trajectories, max_high_y


def sim_trajectory(v_x, v_y, x_target, y_target):
    x = 0
    y = 0
    trajectory = [(x, y)]
    while not ((x_target[0] <= x <= x_target[1]) and (y_target[0] <= y <= y_target[1])):
        x += v_x
        y += v_y
        v_x -= np.sign(v_x)
        v_y -= 1
        trajectory.append((x, y))
        if (v_y < 0) and (y < y_target[0]):
            return None
    return trajectory


def main():
    data = data_folder.joinpath("input.txt").read_text()
    x_target, y_target = parse_data(data)
    n_valid_trajectories, high_y = find_quantities(x_target, y_target)

    print("Part 1")
    print(f"{high_y}")
    print()

    print("Part 2")
    print(f"{n_valid_trajectories}")
    print()


if __name__ == "__main__":
    main()
