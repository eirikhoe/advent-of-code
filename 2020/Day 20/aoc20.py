from os import DirEntry
from pathlib import Path
from copy import deepcopy
from typing import NamedTuple
import numpy as np
from collections import Counter
from itertools import product

DIRECTIONS = ("up", "down", "left", "right")
ROTATIONS = (0, 90, 180, 270)


def get_tile_borders(tile, dir="all"):
    borders = []
    if dir in ["up", "all"]:
        border = min(
            [border_to_id(tile[0, :]), border_to_id(tile[0, ::-1])]
        )
        borders.append(border)
    if dir in ["down", "all"]:
        border = min(
            [border_to_id(tile[-1, :]), border_to_id(tile[-1, ::-1])]
        )
        borders.append(border)
    if dir in ["left", "all"]:
        border = min(
            [border_to_id(tile[:, 0]), border_to_id(tile[::-1, 0])]
        )
        borders.append(border)
    if dir in ["right", "all"]:
        border = min(
            [border_to_id(tile[:, -1]), border_to_id(tile[::-1, -1])]
        )
        borders.append(border)
    if dir != "all":
        return borders[0]
    return borders


def tile_to_id(tile, dir):
    if dir == "up":
        return border_to_id(tile[0, :])
    if dir == "down":
        return border_to_id(tile[-1, :])
    if dir == "left":
        return border_to_id(tile[:, 0])
    if dir == "right":
        return border_to_id(tile[:, -1])


def border_to_id(border):
    return int("".join([str(el) for el in border.astype(int)]), 2)


def rotate(tile, deg, flip_hor=False):
    if deg not in [0, 90, 180, 270]:
        raise RuntimeError("Invalid degrees")
    arr = np.copy(tile)
    if flip_hor:
        arr = arr[:, ::-1]

    if deg == 90:
        return arr[::-1, :].T
    elif deg == 180:
        return arr[::-1, ::-1]
    elif deg == 270:
        return arr[:, ::-1].T
    return arr


class Image:
    def __init__(self, data, pattern):

        self.tiles = dict()
        self.borders = dict()
        self.n_tiles = 0
        self.tile_dim = None

        self.corners = set()
        self.edges = set()
        self.interiors = set()
        self.border_counter = None
        self.corner_prod = None
        id = None
        i = 0
        lines = data.split("\n")
        while i < len(lines):
            if lines[i].startswith("Tile"):
                id = int(lines[i][5:-1])
                i += 1
            tile = []
            while (i < len(lines)) and lines[i]:
                tile.append([int(l == "#") for l in lines[i]])
                i += 1
            if self.tile_dim is None:
                self.tile_dim = len(tile)
            tile = np.array(tile, dtype=np.uint8)
            self.tiles[id] = tile
            self.borders[id] = get_tile_borders(tile)
            self.n_tiles += 1
            i += 1
        for id in self.tiles:
            assert self.tiles[id].shape[0] == self.tile_dim
            assert self.tiles[id].shape[1] == self.tile_dim
        self.puzzle_dim = int(np.round(np.sqrt(self.n_tiles)))
        assert self.puzzle_dim ** 2 == self.n_tiles

        self.solution = np.zeros(
            (self.puzzle_dim, self.puzzle_dim), dtype=int
        )
        self._solve()

        lines = pattern.split("\n")
        self.pattern = []
        for line in lines:
            self.pattern.append([l == "#" for l in line])
        self.pattern = np.array(self.pattern, dtype=bool)

        im_size = self.puzzle_dim * (self.tile_dim - 2)
        self.image = np.zeros((im_size, im_size), dtype=np.uint8)
        self._assemble_image()
        self.n_monsters = self._mark_sea_monsters()

    def _mark_sea_monsters(self):
        orientations = list(product(ROTATIONS, [True, False]))
        n_monsters = 0
        for rot, flip in orientations:
            found_pattern = False
            image = rotate(self.image, rot, flip)
            n_monsters = 0
            for row in range(image.shape[0] - self.pattern.shape[0] + 1):
                for col in range(
                    image.shape[1] - self.pattern.shape[1] + 1
                ):
                    part = image[
                        row : row + self.pattern.shape[0],
                        col : col + self.pattern.shape[1],
                    ]
                    if part[self.pattern].all():
                        part[self.pattern] = 2
                        n_monsters += 1
                        found_pattern = True
            if found_pattern:
                break
        self.image = image
        return n_monsters

    def _check_direction_unique(self, tile, direction):
        id = get_tile_borders(tile, direction)
        return self.border_counter[id] == 1

    def find_habitat_roughness(self):
        return np.sum(self.image == 1)

    def _solve_coord(self, row, col):
        unique_edges = (
            (row == 0)
            + (col == 0)
            + (row == self.puzzle_dim - 1)
            + (col == self.puzzle_dim - 1)
        )
        pieces = None
        if unique_edges == 0:
            pieces = self.interiors
        elif unique_edges == 1:
            pieces = self.edges
        if unique_edges == 2:
            pieces = self.corners
        orientations = list(product(ROTATIONS, [True, False]))
        cand = None
        tile = None
        for cand in pieces:
            valid = False
            for rot, flip in orientations:
                tile = rotate(self.tiles[cand], rot, flip)
                valid = True
                if row == 0:
                    valid &= self._check_direction_unique(tile, "up")
                else:
                    up = self.tiles[self.solution[row - 1, col]]
                    valid &= tile_to_id(tile, "up") == tile_to_id(
                        up, "down"
                    )

                if col == 0:
                    valid &= self._check_direction_unique(tile, "left")
                else:
                    left = self.tiles[self.solution[row, col - 1]]
                    valid &= tile_to_id(tile, "left") == tile_to_id(
                        left, "right"
                    )

                if row == self.puzzle_dim - 1:
                    valid &= self._check_direction_unique(tile, "down")
                if col == self.puzzle_dim - 1:
                    valid &= self._check_direction_unique(tile, "right")

                if valid:
                    break

            if valid:
                break
        self.solution[row, col] = cand
        pieces.remove(cand)
        self.tiles[cand] = tile

    def print_tile(self, image):
        line = []
        char = {1: "#", 0: ".", 2: "O"}
        for row in range(image.shape[0]):
            s = ""
            for col in range(image.shape[1]):
                s += char[image[row, col]]
            line.append(s)
        line.append("")
        output = "\n".join(line)
        print(output)

    def find_corner_product(self):
        corner_prod = 1
        for corner in self.corners:
            corner_prod *= corner
        return corner_prod

    def _assemble_image(self):
        im_col = 0
        for col in range(self.puzzle_dim):
            im_row = 0
            for row in range(self.puzzle_dim):
                tile = np.copy(self.tiles[self.solution[row, col]])[
                    1:-1, 1:-1
                ]
                s = tile.shape
                self.image[
                    im_row : im_row + s[0], im_col : im_col + s[1]
                ] = tile
                im_row += s[0]
            im_col += s[1]

    def _solve(self):
        borders = []
        for id in self.borders:
            borders.extend(self.borders[id])
        self.border_counter = Counter(borders)

        max_edge_count = 0
        for id in self.borders:
            n_unique = 0
            for border in self.borders[id]:
                c = self.border_counter[border]
                n_unique += c == 1
                if c > max_edge_count:
                    max_edge_count = c
            if n_unique == 2:
                self.corners.add(id)
            elif n_unique == 1:
                self.edges.add(id)
            elif n_unique == 0:
                self.interiors.add(id)
        assert max_edge_count == 2

        self.corner_prod = self.find_corner_product()

        dim_range = range(self.puzzle_dim)
        for col, row in product(dim_range, dim_range):
            self._solve_coord(row, col)


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    pattern = data_folder.joinpath("seamonster.txt").read_text()
    t = Image(data, pattern)
    print("Part 1")
    print("The product of the IDs of the four corner ")
    print(f"tiles is {t.corner_prod}")
    print()

    print("Part 2")
    print(f"The habitat's roughness is {t.find_habitat_roughness()}")
    print()

    print(f"Final image with {t.n_monsters} marked sea monsters:")
    t.print_tile(t.image)


if __name__ == "__main__":
    main()
