from pathlib import Path
import numpy as np

data_folder = Path(".").resolve()


def count_increasing_depth(measurements, window_size):
    measurements = np.array(measurements)
    n_measurements = measurements.shape[0]
    windows = np.copy(measurements[: (n_measurements + 1 - window_size)])
    for i in range(1, window_size):
        windows += measurements[i : (n_measurements + 1 - window_size + i)]
    n_increasing = np.sum(np.diff(windows) > 0)
    return n_increasing


def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = [int(d) for d in data.split("\n")]

    measurement_window = 1
    n_increasing = count_increasing_depth(data, measurement_window)

    print("Part 1")
    print(f"{n_increasing} measurements are larger than the previous measurement.")
    print()

    measurement_window = 3
    n_increasing = count_increasing_depth(data, measurement_window)

    print("Part 2")
    print(
        f"{n_increasing} sums of {measurement_window} are larger than the previous sum."
    )
    print()


if __name__ == "__main__":
    main()
