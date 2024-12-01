from pathlib import Path
from collections import deque

data_folder = Path(".").resolve()


def parse_data(data):
    droplet = tuple(tuple(int(d) for d in line.split(",")) for line in data.split("\n"))
    return droplet


def get_neighbours(cube):
    neighbours = []
    for j in range(len(cube)):
        for dir in [1, -1]:
            cand = list(cube)
            cand[j] += dir
            cand = tuple(cand)
            neighbours.append(cand)
    return neighbours


def find_exposed_sides(cube, droplet):
    exposed = []
    for cand in get_neighbours(cube):
        if cand not in droplet:
            exposed.append(cand)
    return exposed


def find_internal(cube, droplet, dims):
    cubes = deque([cube])
    pocket = {cube}
    while len(cubes) > 0:
        current = cubes.pop()
        in_bounds = True
        for i in range(len(current)):
            if not (dims[i][0] < current[i] < dims[i][1]):
                in_bounds = False
                break
        if not in_bounds:
            return None
        for cand in get_neighbours(current):
            if (cand not in droplet) and (cand not in pocket):
                pocket.add(cand)
                cubes.appendleft(cand)
    return pocket


def find_surface_area_droplet(droplet, only_external):
    exposed = []
    for cube in droplet:
        exposed.extend(find_exposed_sides(cube, droplet))
    dims = [
        [min(d), max(d)]
        for d in [[d[i] for d in droplet] for i in range(len(droplet[0]))]
    ]
    surface_area = len(exposed)
    if not only_external:
        return surface_area

    air_pockets = []

    for cand in exposed:
        found = False
        for air_pocket in air_pockets:
            if cand in air_pocket:
                found = True
        if found:
            continue
        new_pocket = find_internal(cand, droplet, dims)
        if new_pocket is not None:
            air_pockets.append(new_pocket)
            surface_area -= find_surface_area_droplet(tuple(new_pocket), False)

    return surface_area


def main():
    data = data_folder.joinpath("input.txt").read_text()
    droplet = parse_data(data)

    print("Part 1")
    surface_area = find_surface_area_droplet(droplet, False)
    print(f"The surface area of the droplet is {surface_area}.")
    print()

    print("Part 2")
    surface_area = find_surface_area_droplet(droplet, True)
    print(f"The exterior surface area of the droplet is {surface_area}.")
    print()


if __name__ == "__main__":
    main()
