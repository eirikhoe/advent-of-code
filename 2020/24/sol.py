from pathlib import Path
import re
from copy import deepcopy
from collections import defaultdict

hex_re = re.compile(r"(ne|se|e|nw|sw|w)")


def get_tile_list(data):
    tile_list = []
    for line in data.split("\n"):
        tile_list.append(hex_re.findall(line))
    return tile_list


def get_tile_coords(directions):
    coord = [0, 0]
    for direction in directions:
        coord = move(direction, coord)
    return tuple(coord)


def move(direction, coord):
    moves = {
        "ne": [-1, 1],
        "se": [1, 1],
        "nw": [-1, 0],
        "sw": [1, 0],
        "e": [0, 1],
        "w": [0, -1],
    }
    if direction in ["ne", "se", "nw", "sw"]:
        coord[1] -= coord[0] % 2
    coord[0] += moves[direction][0]
    coord[1] += moves[direction][1]
    return coord


def get_black_tiles(tile_list):
    black_tiles = set()
    for tile in tile_list:
        coords = get_tile_coords(tile)
        if coords in black_tiles:
            black_tiles.remove(coords)
        else:
            black_tiles.add(coords)
    return black_tiles


def evolve_step(black_tiles):
    directions = ["ne", "se", "nw", "sw", "e", "w"]
    new_state = deepcopy(black_tiles)
    neigh_cand = [0, 0]
    neighbours = defaultdict(lambda: 0)
    for tile in list(black_tiles):
        n_adj_on = 0
        adj_tiles = [move(dir, list(tile)) for dir in directions]
        for adj_tile in adj_tiles:
            if tuple(adj_tile) not in black_tiles:
                neighbours[tuple(adj_tile)] += 1
            else:
                n_adj_on += 1
        if (n_adj_on == 0) or (n_adj_on > 2):
            new_state.remove(tile)
    for neigh in neighbours:
        if neighbours[neigh] == 2:
            new_state.add(neigh)
    black_tiles = new_state
    return black_tiles


def evolve_tiles(black_tiles, n):
    for i in range(n):
        black_tiles = evolve_step(black_tiles)
    return black_tiles


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    tile_list = get_tile_list(data)
    black_tiles = get_black_tiles(tile_list)
    print("Part 1")
    print(f"{len(black_tiles)} tiles are left with the black side up")
    print()

    n_days = 100
    black_tiles = evolve_tiles(black_tiles, n_days)
    print("Part 2")
    print(f"{len(black_tiles)} tiles are black after {n_days} days")


if __name__ == "__main__":
    main()
