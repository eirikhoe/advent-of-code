from pathlib import Path
import numpy as np
from collections import deque

data_folder = Path(".").resolve()


def knot_hash_round(lengths, elements, skip_size=0, index=0):
    n_elements = len(elements)
    elements = deque(elements)
    for j, length in enumerate(lengths):
        elements.rotate(-index)
        reverse = list(elements)[length - 1 :: -1]
        for i in range(length):
            elements[i] = reverse[i]
        elements.rotate(index)
        index = (index + length + skip_size) % n_elements
        skip_size += 1
    return list(elements), skip_size, index


def knot_hash(hash_string):
    lengths = [ord(d) for d in hash_string]
    index = 0
    std_lengths = [17, 31, 73, 47, 23]
    lengths += std_lengths
    skip_size = 0
    n_elements = 256
    elements = list(range(n_elements))
    for i in range(64):
        elements, skip_size, index = knot_hash_round(
            lengths, elements, skip_size, index
        )
    output = ""
    block_len = 16
    n_blocks = 256 // block_len
    for i in range(n_blocks):
        init_ind = i * block_len
        value = elements[init_ind]
        for j in range(init_ind + 1, (i + 1) * block_len):
            value ^= elements[j]
        output += hex(value)[2:].zfill(2)
    return output


def _get_candidates(point):
    return [
        (point[0] - 1, point[1]),
        (point[0], point[1] - 1),
        (point[0], point[1] + 1),
        (point[0] + 1, point[1]),
    ]


class Disk:
    size = 128

    def __init__(self, data):
        self.key_string = data
        self.grid = np.zeros((Disk.size, Disk.size), dtype=int)
        self.build_grid()
        self.n_regions = 0
        self.regions = np.zeros((Disk.size, Disk.size), dtype=int)
        self.find_regions()
    def build_grid(self):
        for row in range(Disk.size):
            hash_string = f"{self.key_string}-{row}"
            hashed_string = knot_hash(hash_string)
            self.grid[row] = self.to_bits(hashed_string)

    def to_bits(self, hashed_string):
        bit_vector = np.zeros((1, Disk.size), dtype=int)
        for i, hex_char in enumerate(list(hashed_string)):
            bit_string = bin(int(hex_char, 16))[2:].zfill(4)
            bit_vector[0, i * 4 : (i + 1) * 4] = [int(d) for d in bit_string]
        return bit_vector

    def find_regions(self):
        for row in range(Disk.size):
            for col in range(Disk.size):
                if (not self.regions[row, col]) and self.grid[row, col]:
                    self.n_regions += 1
                    self.bfs((row, col))

    def bfs(self, pos):
        queue = deque([pos])
        while len(queue) > 0:
            point = queue.popleft()
            for candidate in _get_candidates(point):
                if (max(candidate[0],candidate[1]) >= Disk.size) or (min(candidate[0],candidate[1]) < 0):
                    continue

                if (not self.regions[candidate]) and self.grid[candidate]:
                    self.regions[candidate] = self.n_regions
                    queue.append(candidate)

    def print_grid(self, regions=False):
        symbols = [".", "#"]
        s = ""
        col_size = Disk.size
        col_digits = len(str(col_size))
        row_size = Disk.size
        row_digits = len(str(row_size))

        form_str = "{:" + str(col_digits) + "d}"
        chr_count = 0
        for j in range(col_digits):
            s += " " * row_digits
            for loc in range(col_size):
                loc_str = form_str.format(loc)
                s += loc_str[j]
            s += "\n"

        form_str = "{:" + str(row_digits) + "d}"
        for y in range(row_size):
            s += form_str.format(y)

            if regions:
                for k in self.regions[y]:
                    if not k:
                        s += symbols[k]
                    else:
                        s += chr((k % (126-49)) + 49)

            else:
                for k in self.grid[y]:
                    s += symbols[k]
            s += "\n"
        data_folder = Path(".").resolve()
        data_folder.joinpath("output.txt").write_text(s)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    d = Disk(data)
    print("Part 1")
    print(
        f"{np.sum(d.grid)} squares are used across the entire {Disk.size}x{Disk.size} grid"
    )
    print()

    print("Part 2")
    d.print_grid(regions=True)
    print(
        f"There are {d.n_regions} regions on the disk"
    )


if __name__ == "__main__":
    main()
