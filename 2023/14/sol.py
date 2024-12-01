from pathlib import Path
import copy

data_folder = Path(".").resolve()


def parse_data(data):
    platform = [list(line) for line in data.split("\n")]
    return platform


def slide_row(row):
    free_loc = 0
    for i, char in enumerate(row):
        if char == "O":
            temp = row[free_loc]
            row[free_loc] = "O"
            row[i] = temp
            free_loc += 1
        elif char == "#":
            free_loc = i + 1
    return row


def rotate_90(platform):
    n = len(platform)
    m = len(platform[0])
    rotated = [["."] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            rotated[i][j] = platform[n - j - 1][i]
    return rotated


def spin_cycle(platform):
    for _ in range(4):
        platform = slide_north(platform)
        platform = rotate_90(platform)
    return platform


def slide_north(platform):
    platform = copy.deepcopy(platform)
    for j, _ in enumerate(platform[0]):
        col = [platform[i][j] for i, _ in enumerate(platform)]
        slided_col = slide_row(col)
        for i, _ in enumerate(platform):
            platform[i][j] = slided_col[i]
    return platform


def print_platform(platform):
    s = []
    for i, _ in enumerate(platform):
        s.append("".join(platform[i]))
    print("\n".join(s))


def hash_platform(platform):
    s = ""
    for i, _ in enumerate(platform):
        s += "".join(platform[i])
    return s


def compute_total_north_load(platform):
    north_load = 0
    for i, _ in enumerate(platform):
        for j, char in enumerate(platform[i]):
            if char == "O":
                north_load += len(platform) - i
    return north_load


def repeat_spin_cycles(platform, n_iter):
    platform = copy.deepcopy(platform)
    seen = {hash_platform(platform): 0}
    for i in range(n_iter):
        platform = spin_cycle(platform)
        id = hash_platform(platform)
        if id not in seen:
            seen[id] = i + 1
        else:
            period = (i + 1) - seen[id]
            break
    remaining = (n_iter - (i + 1)) % period
    for i in range(remaining):
        platform = spin_cycle(platform)
    return platform


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    platform = parse_data(data)

    print("Part 1")
    north_slide_platform = slide_north(platform)
    north_load = compute_total_north_load(north_slide_platform)
    print(
        f"The total load on the north support beams after a north slide "
        f"is {north_load}."
    )
    print()

    print("Part 2")
    n_iter = 1000000000
    spun_platform = repeat_spin_cycles(platform, n_iter)
    north_load = compute_total_north_load(spun_platform)
    print(
        f"The total load on the north support beams after {n_iter} spin cycles "
        f"is {north_load}."
    )


if __name__ == "__main__":
    main()
