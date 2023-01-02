from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    lines = data.split("\n")
    elves = set()
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if char == "#":
                elves.add((row, col))
    return elves


def move_elf(elf, current_elves, first_dir):
    move_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    n_dir = len(move_directions)
    taken = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0) and (j == 0):
                continue
            cand = (elf[0] + i, elf[1] + j)
            if cand in current_elves:
                if i != 0:
                    taken.add((i, 0))
                if j != 0:
                    taken.add((0, j))
    if not taken:
        return elf
    for i in range(n_dir):
        index = (first_dir + i) % n_dir
        direction = move_directions[index]
        if direction not in taken:
            return (elf[0] + direction[0], elf[1] + direction[1])
    return elf


def move_elves(current_elves, dir_offset):
    new_moves = dict()
    need_move = False
    for elf in current_elves:
        moved_elf = move_elf(elf, current_elves, dir_offset)
        if (not need_move) and (moved_elf != elf):
            need_move = True
        if moved_elf in new_moves:
            new_moves[moved_elf].add(elf)
        else:
            new_moves[moved_elf] = {elf}
    elves = set()
    for dest, origin in new_moves.items():
        if len(origin) > 1:
            elves = elves.union(origin)
        else:
            elves.add(dest)
    return elves, need_move


def find_stable_elf_distribution(elves, max_iter=None):
    need_move = True
    i = 0
    while need_move:
        elves, need_move = move_elves(elves, i)
        i += 1
        if (max_iter is not None) and (i == max_iter):
            break
    return elves, i


def find_rectangle_empty_tiles(elves):
    min_col = min([p[1] for p in elves])
    max_col = max([p[1] for p in elves])
    min_row = min([p[0] for p in elves])
    max_row = max([p[0] for p in elves])
    empty_tiles = 0
    for y in range(min_row - 0, max_row + 1):
        for x in range(min_col - 0, max_col + 1):
            empty_tiles += int((y, x) not in elves)
    return empty_tiles


def print_grid(elves):
    s = ""
    min_col = min([p[1] for p in elves])
    max_col = max([p[1] for p in elves])
    min_row = min([p[0] for p in elves])
    max_row = max([p[0] for p in elves])

    for y in range(min_row - 0, max_row + 1):
        for x in range(min_col - 0, max_col + 1):
            s += "#" if (y, x) in elves else "."
        s += "\n"
    s += "\n"
    data_folder.joinpath("output.txt").write_text(s)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    elves = parse_data(data)

    print("Part 1")
    stable, _ = find_stable_elf_distribution(elves, max_iter=10)
    n_empty = find_rectangle_empty_tiles(stable)
    print(f"The smallest rectangle with all elves contains {n_empty} ground tiles.")
    print()

    print("Part 2")
    stable, n_iter = find_stable_elf_distribution(elves)
    print(f"The number of the first round where no Elf moves is {n_iter}.")
    print()


if __name__ == "__main__":
    main()
