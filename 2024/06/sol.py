from pathlib import Path
import copy

data_folder = Path(".").resolve()


def parse_data(data):
    grid = [list(row) for row in data.split("\n")]
    return grid


def find_start_pos(grid):
    for i, row in enumerate(grid):
        try:
            ind = row.index("^")
            break
        except ValueError:
            continue
    return (i, ind)


def on_grid(grid, pos):
    return (0 <= pos[0] < len(grid)) and (0 <= pos[1] < len(grid[0]))


def is_valid(grid, pos):
    on = on_grid(grid,pos)
    return (on and (grid[pos[0]][pos[1]] == ".")) or (not on)


def make_move(grid, pos, dir):
    new_pos = (pos[0] + dir[0], pos[1] + dir[1])
    while not is_valid(grid, new_pos):
        dir = turn_right(dir)
        new_pos = (pos[0] + dir[0], pos[1] + dir[1])
    return new_pos, dir


def turn_right(dir):
    return (dir[1], -dir[0])

def move_until_off_grid_or_loop(grid,start_pos):
    grid[start_pos[0]][start_pos[1]] = "."
    seen = {start_pos}
    pos = start_pos
    dir = (-1,0)
    dir_seen = set()
    while on_grid(grid,pos) and ((pos,dir) not in dir_seen):
        dir_seen.add((pos,dir))
        pos, dir = make_move(grid,pos,dir)
        seen.add(pos)
    if (pos,dir) in dir_seen:
        return None
    seen.remove(pos)
    return seen 

def remove_start_pos(grid,start_pos):
    grid = copy.deepcopy(grid)
    grid[start_pos[0]][start_pos[1]] = "."
    return grid

def count_seen(grid):
    start_pos = find_start_pos(grid)
    grid = remove_start_pos(grid,start_pos)
    seen = move_until_off_grid_or_loop(grid,start_pos)
    return len(seen)


def find_possible_loops(grid):
    start_pos = find_start_pos(grid)
    grid = remove_start_pos(grid,start_pos)
    seen = move_until_off_grid_or_loop(grid,start_pos)
    seen.remove(start_pos)
    count = 0
    for pos in seen:
        new_grid = copy.deepcopy(grid)
        new_grid[pos[0]][pos[1]] = "#"
        count += (move_until_off_grid_or_loop(new_grid,start_pos) is None)
    return count


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    grid = parse_data(data)

    print("Part 1")
    print(f"The guard will visit {count_seen(grid)} distinct positions before leaving.")
    print()

    print("Part 2")
    print(f"{find_possible_loops(grid)} possible obstruction positions result in a loop.")
    print()


if __name__ == "__main__":
    main()
