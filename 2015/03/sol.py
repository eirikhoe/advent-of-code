from pathlib import Path

data_folder = Path(".").resolve()


def count_present_locations(data, n_santas=1):
    pos = [(0, 0)] * n_santas
    visited = {pos[0]}
    direction = {"<": (0, -1), "^": (-1, 0), "v": (1, 0), ">": (0, 1)}
    for i, char in enumerate(data):
        v = direction[char]
        santa = i % n_santas
        pos[santa] = (pos[santa][0] + v[0], pos[santa][1] + v[1])
        visited.add(pos[santa])
    return len(visited)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    print("Part 1")
    n_locs = count_present_locations(data)
    print(f"{n_locs} houses receive at least one present")
    print()

    print("Part 2")
    n_locs = count_present_locations(data, 2)
    print(f"{n_locs} houses receive at least one present using Robo-Santa")


if __name__ == "__main__":
    main()
