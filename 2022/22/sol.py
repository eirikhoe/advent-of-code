from pathlib import Path
from copy import deepcopy

data_folder = Path(".").resolve()

vec_to_symb = {(0, 1): ">", (0, -1): "<", (-1, 0): "^", (1, 0): "v"}
vec_to_value = {(0, 1): 0, (0, -1): 2, (-1, 0): 3, (1, 0): 1}
rotated = [(0, 1), (-1, 0), (0, -1), (1, 0)]

standard_cube_map = [
    {(0, 1): (3, 270), (0, -1): (1, 90), (-1, 0): (5, 0), (1, 0): (2, 0)},
    {(0, 1): (2, 0), (0, -1): (5, 180), (-1, 0): (0, 270), (1, 0): (4, 90)},
    {(0, 1): (3, 0), (0, -1): (1, 0), (-1, 0): (0, 0), (1, 0): (4, 0)},
    {(0, 1): (5, 180), (0, -1): (2, 0), (-1, 0): (0, 90), (1, 0): (4, 270)},
    {(0, 1): (3, 90), (0, -1): (1, 270), (-1, 0): (2, 0), (1, 0): (5, 0)},
    {(0, 1): (3, 180), (0, -1): (1, 180), (-1, 0): (4, 0), (1, 0): (0, 0)},
]


def turn(v, direction):
    if direction not in ["R", "L"]:
        raise RuntimeError("Invalid direction")
    deg = 90 if direction == "L" else 270
    return turn_left(v, deg)


def turn_left(v, deg):
    if deg not in [0, 90, 180, 270]:
        raise RuntimeError("Invalid degrees")

    if deg == 90:
        return (-v[1], v[0])
    elif deg == 180:
        return (-v[0], -v[1])
    elif deg == 270:
        return (v[1], -v[0])
    return v


def make_cube(board):
    n_rows = len(board)
    n_cols = len(board[0])
    if min(n_rows, n_cols) * 4 != max(n_rows, n_cols) * 3:
        raise RuntimeError("Dimensions not compatible")
    face_len = min(n_rows, n_cols) // 3
    has_side = []
    first_side = True
    start = None

    for i in range(n_rows // face_len):
        has_side.append([])
        for j in range(n_cols // face_len):
            has_side[-1].append(
                int(board[i * face_len + face_len // 2][j * face_len + face_len // 2] != " ")
            )
            if (has_side[-1][-1] != 0) and first_side:
                start = (i, j)
                first_side = False

    sides = [None for _ in range(6)]
    sides[0] = (start, 0)
    candidates = [(start, 0, 0)]
    while len(candidates) > 0:
        curr = candidates.pop()
        has_side[curr[0][0]][curr[0][1]] = 0
        for dir in rotated:
            cand = (curr[0][0] + dir[0], curr[0][1] + dir[1])
            if (
                (not (0 <= cand[0] < len(has_side)))
                or (not (0 <= cand[1] < len(has_side[0])))
                or (not bool(has_side[cand[0]][cand[1]]))
            ):
                continue
            cand_dir = turn_left(dir, curr[2])
            side = standard_cube_map[curr[1]][cand_dir][0]
            cand_dir = turn_left(dir, 180)
            rotation = 0
            while standard_cube_map[side][cand_dir][0] != curr[1]:
                rotation += 90
                cand_dir = turn(cand_dir, "L")
            sides[side] = (cand, rotation)
            candidates.append((cand, side, rotation))

    return sides, face_len


def parse_data(data):
    lines = data.split("\n")
    board = [list(line) for line in lines[:-2]]
    n_cols = max(map(len, board))
    for i, _ in enumerate(board):
        board[i] += [" " for _ in range(n_cols - len(board[i]))]
    instr = []
    num = ""
    for char in lines[-1]:
        if char in ["R", "L"]:
            if len(num) > 0:
                instr.append(int(num))
                num = ""
            instr.append(char)
        else:
            num += char
    if len(num) > 0:
        instr.append(int(num))

    return board, instr


def valid_coord(board, pos):
    return (
        (0 <= pos[0] < len(board))
        and (0 <= pos[1] < len(board[pos[0]]))
        and (board[pos[0]][pos[1]] != " ")
    )


def move(board, instr, pos, dir, journey, cube_map, face_len):
    if instr in ["R", "L"]:
        dir = turn(dir, instr)
        instr = 0
    for _ in range(instr):
        journey[pos[0]][pos[1]] = vec_to_symb[dir]
        cand = deepcopy(pos)
        cand[0] = pos[0] + dir[0]
        cand[1] = pos[1] + dir[1]
        changed_dir = False
        if not valid_coord(board, cand):
            cand = deepcopy(pos)
            if cube_map is None:
                reverse = turn_left(dir, 180)
                while valid_coord(board, cand):
                    new_cand = deepcopy(cand)
                    cand[0] += reverse[0]
                    cand[1] += reverse[1]
                cand = new_cand
            else:
                cube_map_coord = tuple(cand[i] // face_len for i in range(2))

                # Multiply centered coordinated by 2 to avoid non integers
                double_side_coord = tuple(
                    2 * (cand[i] % face_len) - (face_len - 1) for i in range(2)
                )
                for side, _ in enumerate(cube_map):
                    if cube_map[side][0] == cube_map_coord:
                        break
                standard_dir = turn_left(dir, cube_map[side][1])
                new_side, standard_rot = standard_cube_map[side][standard_dir]
                mapped_dir = turn_left(standard_dir, (standard_rot - cube_map[new_side][1]) % 360)
                total_rot = (cube_map[side][1] + standard_rot - cube_map[new_side][1]) % 360
                new_double_side_coord = list(turn_left(double_side_coord, total_rot))
                i = 0 if mapped_dir[0] != 0 else 1
                new_double_side_coord[i] = -new_double_side_coord[i]
                cand = [
                    (
                        2 * face_len * cube_map[new_side][0][i]
                        + (face_len - 1)
                        + new_double_side_coord[i]
                    )
                    // 2
                    for i in range(2)
                ]
                changed_dir = True

        if board[cand[0]][cand[1]] == "#":
            break
        elif changed_dir:
            dir = mapped_dir
            changed_dir = False
        pos = cand
    journey[pos[0]][pos[1]] = vec_to_symb[dir]
    return pos, dir, journey


def follow_instructions(instrs, board, cube_map=None, face_len=None):
    journey = deepcopy(board)
    dir = (0, 1)
    for i, char in enumerate(board[0]):
        if char == ".":
            break
    pos = [0, i]
    journey[pos[0]][pos[1]] = vec_to_symb[dir]
    for instr in instrs:
        pos, dir, journey = move(board, instr, pos, dir, journey, cube_map, face_len)
    return pos, dir, journey


def compute_password(pos, dir):
    row = 1 + pos[0]
    col = 1 + pos[1]
    return 1000 * row + 4 * col + vec_to_value[dir]


def print_journey(journey):
    s = "\n".join(["".join(line) for line in journey])
    file = data_folder / "output.txt"
    file.write_text(s)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    board, instrs = parse_data(data)

    print("Part 1")
    pos, dir, _ = follow_instructions(instrs, board)
    password = compute_password(pos, dir)
    print(f"The password is {password}.")
    print()

    print("Part 2")
    cube_map, face_len = make_cube(board)
    pos, dir, _ = follow_instructions(instrs, board, cube_map, face_len)
    password = compute_password(pos, dir)
    print(f"The password is {password}.")
    print()


if __name__ == "__main__":
    main()
