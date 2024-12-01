from pathlib import Path
import numpy as np
import re
from collections import defaultdict
import re

reg = re.compile(r"([#./]+) => ([#./]+)")


class Fractals:
    symbols = {"#": 1, ".": 0}
    inv_symbols = {1: "#", 0: "."}

    def __init__(self, data):
        self.rules_start = {2: [], 3: []}
        self.rules_end = {2: [], 3: []}
        self.image = np.array([[0, 1, 0], [0, 0, 1], [1, 1, 1]], dtype=int)

        for line in data.split("\n"):
            m = reg.match(line)
            rule_start = []
            for row in m.group(1).split("/"):
                rule_start.append([])
                for char in list(row):
                    rule_start[-1].append(Fractals.symbols[char])
            self.rules_start[len(rule_start)].append(rule_start)

            rule_end = []
            for row in m.group(2).split("/"):
                rule_end.append([])
                for char in list(row):
                    rule_end[-1].append(Fractals.symbols[char])
            self.rules_end[len(rule_start)].append(rule_end)

        for key in self.rules_start:
            self.rules_start[key] = np.array(self.rules_start[key], dtype=int)
            self.rules_end[key] = np.array(self.rules_end[key], dtype=int)

    def step(self):
        size = self.image[0].size
        if size % 2 == 0:
            square_size = 2
            new_square_size = 3
        else:
            square_size = 3
            new_square_size = 4

        new_size = new_square_size * size // square_size
        new_image = np.zeros((new_size, new_size), dtype=int)
        n_parts = size // square_size
        for i in np.arange(n_parts):
            for j in np.arange(n_parts):
                square = self.image[
                    i * square_size : (i + 1) * square_size,
                    j * square_size : (j + 1) * square_size,
                ]
                rotations = self.gen_rotations(square)
                for k in np.arange(self.rules_start[square_size].shape[0]):
                    rule = self.rules_start[square_size][k][:, :, np.newaxis]
                    if np.any(
                        np.all(np.all(rule == rotations, axis=0), axis=0), axis=0
                    ):
                        new_image[
                            i * new_square_size : (i + 1) * new_square_size,
                            j * new_square_size : (j + 1) * new_square_size,
                        ] = self.rules_end[square_size][k]
                        break
        self.image = new_image

    def evolve(self, n):
        for i in range(n):
            self.step()

    def gen_rotations(self, square):
        rotations = np.zeros((*square.shape, 8), dtype=int)
        rotations[:, :, 0] = square
        rotations[:, :, 1] = square.T[:, ::-1]
        rotations[:, :, 2] = square[::-1, ::-1]
        rotations[:, :, 3] = square.T[::-1]
        rotations[:, :, 4] = square[::-1, :]
        rotations[:, :, 5] = square.T
        rotations[:, :, 6] = square[:, ::-1]
        rotations[:, :, 7] = square.T[::-1, ::-1]
        return rotations

    def print_image(self, file=True):
        image = np.copy(self.image)
        s = ""
        col_size = image.shape[1]

        row_size = image.shape[0]
        for y in range(row_size):
            for x in range(col_size):
                s += Fractals.inv_symbols[image[y, x]]
            s += "\n"
        print(s)

    def count_on_pixels(self):
        return np.sum(self.image)


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    f = Fractals(data)
    print("Part 1")
    n_iterations = 5
    f.evolve(n_iterations)

    print("Image")
    f.print_image()
    print(f"{f.count_on_pixels()} pixels stay on after {n_iterations} iterations")
    print()

    print("Part 2")
    additional_iterations = 18 - n_iterations
    f.evolve(additional_iterations)
    print(
        f"{f.count_on_pixels()} pixels stay on after {n_iterations+additional_iterations} iterations"
    )


if __name__ == "__main__":
    main()
