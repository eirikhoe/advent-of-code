from pathlib import Path
import copy

data_folder = Path(".").resolve()

dirs = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}
reverse = {"N": "S", "E": "W", "S": "N", "W": "E"}

tiles = {
    "|": ("N", "S"),
    "-": ("E", "W"),
    "L": ("N", "E"),
    "J": ("N", "W"),
    "7": ("S", "W"),
    "F": ("S", "E"),
}


def update_pos(pos, dir):
    step = dirs[dir]
    return (pos[0] + step[0], pos[1] + step[1])


def follow_pipe(pos, field, dir):
    new_pos = update_pos(pos, dir)
    tile = field[new_pos[0]][new_pos[1]]
    if tile == "S":
        return new_pos, None, "S"
    came_from = reverse[dir]
    new_dir = list(set(tiles[tile]) - set([came_from]))[0]
    return new_pos, new_dir, tile


def find_start_pos(field):
    for i, line in enumerate(field):
        for j, pipe in enumerate(line):
            if pipe == "S":
                return (i, j)


def is_valid(pos, field):
    return (0 <= pos[0] < len(field)) and (0 <= pos[1] < len(field[pos[0]]))


def find_start_tile(field, start_pos):
    valid_dirs = []
    for dir in dirs:
        new_pos = update_pos(start_pos, dir)
        neighbour = field[new_pos[0]][new_pos[1]]
        reverse_dir = reverse[dir]
        if (
            is_valid(new_pos, field)
            and (neighbour in tiles)
            and (reverse_dir in tiles[neighbour])
        ):
            valid_dirs.append(dir)
    assert len(valid_dirs) == 2
    for tile, tile_dirs in tiles.items():
        if set(tile_dirs) == set(valid_dirs):
            return tile


def find_distances(start_pos, tile, field, initial_dir, distances):
    pos = start_pos
    dir = initial_dir
    distances[start_pos] = 0
    dist = 0
    while tile != "S":
        pos, dir, tile = follow_pipe(pos, field, dir)
        dist += 1
        if (pos not in distances) or (dist < distances[pos]):
            distances[pos] = dist
    return distances


def find_furthest_tile(field):
    start_pos = find_start_pos(field)
    start_tile = find_start_tile(field, start_pos)
    distances = dict()
    for initial_dir in tiles[start_tile]:
        distances = find_distances(start_pos, start_tile, field, initial_dir, distances)
    max_dist = 0
    for _, distance in distances.items():
        if distance > max_dist:
            max_dist = distance
    return max_dist

def count_inside(field):
    start_pos = find_start_pos(field)
    start_tile = find_start_tile(field,start_pos)
    distances = dict()
    initial_dir = tiles[start_tile][0]
    distances = find_distances(start_pos,start_tile,field,initial_dir,distances)
    field = copy.deepcopy(field)
    field[start_pos[0]][start_pos[1]] = start_tile
    loop = set(distances.keys())
    inside_count = 0
    for i,_ in enumerate(field):
        inside = False
        j = 0
        while j < len(field[i]):
            if ((i,j) not in loop): 
                inside_count += int(inside)
                j += 1
                continue
            if field[i][j] == "|":
                inside = (not inside)
                j += 1
            else:
                first_tile = field[i][j]
                j += 1
                while field[i][j] == "-":
                    j += 1
                second_tile = field[i][j]
                if len(set(tiles[first_tile]).intersection(tiles[second_tile])) == 0:
                    inside = (not inside)
                j += 1
    return inside_count

def parse_data(data):
    field = [list(line) for line in data.split("\n")]
    return field


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    field = parse_data(data)

    print("Part 1")
    furthest_tile = find_furthest_tile(field)
    print(f"The tile furthest away along the loop is {furthest_tile} tiles away.")
    print()

    print("Part 2")
    print(f"There are {count_inside(field)} tiles inside the loop.")
    print()


if __name__ == "__main__":
    main()
