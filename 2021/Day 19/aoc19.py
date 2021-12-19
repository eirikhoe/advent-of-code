from pathlib import Path
import numpy as np
import itertools
from copy import deepcopy

data_folder = Path(".").resolve()

FACE_ROTS = [("x", 0), ("x", 90), ("x", 180), ("x", 270), ("y", 90), ("y", 270)]
Z_ROTS = [0, 90, 180, 270]


def parse_data(data):
    beacon_maps_data = data.split("\n\n")
    beacon_maps = []
    for beacon_map_data in beacon_maps_data:
        beacon_map = []
        for line in beacon_map_data.split("\n")[1:]:
            beacon_map.append(list(eval(line)))
        beacon_maps.append(np.array(beacon_map))
    return beacon_maps


def get_rot_matrix(axis, deg):
    ind = deg // 90
    cosines = [1, 0, -1, 0]
    sines = [0, 1, 0, -1]
    c = cosines[ind]
    s = sines[ind]
    if axis == "x":
        r = np.array([[1, 0, 0], [0, c, -s], [0, s, c]]).transpose()
    elif axis == "y":
        r = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]]).transpose()
    elif axis == "z":
        r = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]]).transpose()
    return r


def align_all_beacon_maps(beacon_maps):
    n_beacon_maps = len(beacon_maps)
    align_recipes = []
    new_beacon_maps = [beacon_maps[0]]
    used = [0]
    ind = 0
    while ind < len(used):
        for j in range(1, n_beacon_maps):
            if j in used:
                continue
            res = try_to_align(beacon_maps[used[ind]], beacon_maps[j])
            if res is not None:
                align_recipes.append([ind, *res])
                used.append(j)
                new_beacon_maps.append(beacon_maps[j])
        ind += 1
    beacon_maps = new_beacon_maps
    scanner_locations = [np.array([0, 0, 0]).reshape((1, -1)) for _ in range(n_beacon_maps)]
    for j in range(n_beacon_maps - 2, -1, -1):
        beacon_maps, scanner_locations = align_and_add(
            beacon_maps, scanner_locations, j, *align_recipes[j]
        )
    beacon_maps = np.unique(beacon_maps[0], axis=0)
    max_dist = 0
    scanner_locations = scanner_locations[0]
    for i in range(1, scanner_locations.shape[0]):
        for j in range(i):
            d = manhattan_distance(scanner_locations[i], scanner_locations[j])
            if d > max_dist:
                max_dist = d
    return beacon_maps.shape[0], max_dist


def manhattan_distance(first, second):
    return np.sum(np.abs(first - second))


def _align_and_add(data, i, face_rot, z_rot, align, j):
    d = data.pop(j + 1)
    aligned_data = rotate_beacon_map(face_rot, z_rot, d)
    aligned_data += align
    data[i] = np.vstack([data[i], aligned_data])
    return data


def align_and_add(beacon_maps, scanner_locations, j, *args):
    i, face_rot, z_rot, align = args
    beacon_maps = _align_and_add(beacon_maps, i, face_rot, z_rot, align, j)
    scanner_locations = _align_and_add(scanner_locations, i, face_rot, z_rot, align, j)
    return beacon_maps, scanner_locations


def try_to_align(fixed_beacon_map, beacon_map):
    for face_rot, z_rot in itertools.product(FACE_ROTS, Z_ROTS):
        rot_beacon_map = rotate_beacon_map(face_rot, z_rot, beacon_map)
        for alignment in align_beacon_map(fixed_beacon_map, rot_beacon_map):
            aligned_beacon_map = rot_beacon_map + alignment
            if is_alignment_found(fixed_beacon_map, aligned_beacon_map):
                return face_rot, z_rot, alignment


def rotate_beacon_map(face_rot, z_rot, beacon_map):
    rot_beacon_map = np.copy(beacon_map)
    if face_rot[1] > 0:
        R_face = get_rot_matrix(face_rot[0], face_rot[1])
        rot_beacon_map = beacon_map @ R_face
    if z_rot > 0:
        R_z = get_rot_matrix("z", z_rot)
        rot_beacon_map = rot_beacon_map @ R_z
    return rot_beacon_map


def align_beacon_map(fixed_beacon_map, beacon_map):
    for fp, p in itertools.product(fixed_beacon_map, beacon_map):
        yield fp - p


def is_alignment_found(fixed_beacon_map, beacon_map):
    unq, counts = np.unique(np.vstack([fixed_beacon_map, beacon_map]), axis=0, return_counts=True)
    aligned = unq[counts == 2].shape[0] >= 12
    return aligned


def main():
    data = data_folder.joinpath("input.txt").read_text()
    beacon_maps = parse_data(data)

    print("Part 1")
    n_beacons, largest_scanner_distance = align_all_beacon_maps(beacon_maps)
    print(f"There are {n_beacons} beacons on the full map")
    print()

    print("Part 2")
    print(
        f"The largest manhattan distance between two beacon_maps is {largest_scanner_distance} units"
    )
    print()


if __name__ == "__main__":
    main()
