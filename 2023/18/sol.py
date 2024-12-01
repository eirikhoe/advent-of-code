from pathlib import Path

DIRS = {"R": (0, 1), "L": (0, -1), "D": (1, 0), "U": (-1, 0)}
VAL_TO_DIR = "RDLU"

data_folder = Path(".").resolve()


def parse_data(data):
    instrs = [line.split() for line in data.split("\n")]
    for i, _ in enumerate(instrs):
        instrs[i][1] = int(instrs[i][1])
        instrs[i][2] = instrs[i][2][2:-1]
    return instrs


def update_pos(pos, dir, length):
    return tuple([pos[k] + length * dir[k] for k in range(2)])


def dig_edges(instrs, use_color=False):
    pos = (0, 0)
    corners = [[pos, set()]]

    for i, instr in enumerate(instrs):
        if use_color:
            length = int(instr[2][:5], 16)
            index = int(instr[2][5], 16)
            dir_char = VAL_TO_DIR[index]
        else:
            dir_char = instr[0]
            length = instr[1]
        direction = DIRS[dir_char]
        corners[-1][1].add(dir_char)
        if i > 0 and (len(corners[-1][1]) == 1):
            corners.pop()
        pos = update_pos(pos, direction, length)
        corners.append([pos, set()])
        corners[-1][1].add(dir_char)
    end = corners.pop()
    corners[0][1] = corners[0][1].union(end[1])
    if len(corners[0][1]) == 1:
        corners.pop(0)
    return corners


def is_boundary(pos, corners, index):
    n = len(corners)
    for i in range(n):
        j = (i + 1) % n
        if not (corners[i][0][1 - index] == corners[j][0][1 - index] == pos[1 - index]):
            continue
        lower = min(corners[i][0][index], corners[j][0][index])
        higher = max(corners[i][0][index], corners[j][0][index])
        if lower < pos[index] < higher:
            return True
    return False


def is_corner(pos, corners):
    for i, c in enumerate(corners):
        if pos == c[0]:
            return i
    return None


def find_volume(corners):
    vert_corner_coords = sorted(list(set([c[0][0] for c in corners])))
    hor_corner_coords = sorted(list(set([c[0][1] for c in corners])))
    volume = 0
    for i, v in enumerate(vert_corner_coords):
        volume += get_boundary_len(hor_corner_coords, corners, v)
        if i == (len(vert_corner_coords) - 1):
            continue
        h = vert_corner_coords[i + 1] - v
        if h > 1:
            volume += (h - 1) * get_boundary_len(hor_corner_coords, corners, v + 1)
    return volume


def get_boundary_len(hor_corner_coords, corners, v):
    n = len(corners)
    edges = []
    j = 0
    inside = False
    while j < len(hor_corner_coords):
        h = hor_corner_coords[j]
        index = is_corner((v, h), corners)
        if index is None:
            if is_boundary((v, h), corners, 0):
                edges.append(h)
                inside = not inside
            j += 1
            continue
        if not inside:
            edges.append(h)
        if "R" in corners[index][1]:
            other = (index + 1) % n
        else:
            other = (index - 1) % n
        while hor_corner_coords[j] < corners[other][0][1]:
            j += 1
        if corners[index][1] == corners[other][1]:
            inside = not inside
        if not inside:
            edges.append(hor_corner_coords[j])
        j += 1
    length = sum([edges[k + 1] - edges[k] + 1 for k in range(0, len(edges), 2)])
    return length


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    instrs = parse_data(data)
    print("Part 1")
    corners = dig_edges(instrs, use_color=False)
    volume = find_volume(corners)
    print(f"The trench volume using the original instructions is {volume}.")
    print()

    print("Part 2")
    corners = dig_edges(instrs, use_color=True)
    volume = find_volume(corners)
    print(f"The trench volume using the hexadecimal instructions is {volume}.")
    print()


if __name__ == "__main__":
    main()
