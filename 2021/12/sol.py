from pathlib import Path
from collections import defaultdict

data_folder = Path(".").resolve()


def parse_data(data):
    cave_connections = [line.split("-") for line in data.split("\n")]
    connected_to = defaultdict(list)
    for line in cave_connections:
        connected_to[line[0]].append(line[1])
        connected_to[line[1]].append(line[0])
    return connected_to


def find_cave_paths(connected_to, visited, lower_twice_allowed, lower_twice_already):
    if visited[-1] == "end":
        return 1
    n_paths = 0
    for candidate in connected_to[visited[-1]]:
        lower_twice = lower_twice_already
        if candidate == "start":
            continue
        if (candidate == candidate.lower()) and (candidate in visited):
            if (not lower_twice_allowed) or lower_twice:
                continue
            else:
                lower_twice = True
        new_visited = visited + [candidate]
        n_paths += find_cave_paths(
            connected_to, new_visited, lower_twice_allowed, lower_twice
        )
    return n_paths


def main():
    data = data_folder.joinpath("input.txt").read_text()
    connected_to = parse_data(data)

    print("Part 1")
    n_paths = find_cave_paths(connected_to, ["start"], False, False)
    print(
        f"There are {n_paths} paths through this cave system that visit small caves at most once."
    )
    print()

    print("Part 2")
    n_paths = find_cave_paths(connected_to, ["start"], True, False)
    print(
        f"There are {n_paths} paths through this cave system that visit at most one small cave twice."
    )
    print()


if __name__ == "__main__":
    main()
