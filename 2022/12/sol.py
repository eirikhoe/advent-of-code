from pathlib import Path
import bisect
import string
from collections import deque

data_folder = Path(".").resolve()
char_to_int = dict(zip(string.ascii_lowercase, range(26)))


def parse_data(data):
    scan = []
    start = None
    end = None
    for i, line in enumerate(data.split("\n")):
        scan.append([])
        for j, char in enumerate(line):
            if char == "S":
                start = (i, j)
                char = "a"
            elif char == "E":
                end = (i, j)
                char = "z"
            scan[-1].append(char_to_int[char])
    return scan, start, end


def get_candidates(pos, scan):
    candidates = []
    height_limit = scan[pos[0]][pos[1]] + 1
    if (pos[0] < len(scan) - 1) and (scan[pos[0] + 1][pos[1]] <= height_limit):
        candidates.append((pos[0] + 1, pos[1]))
    if (pos[1] < len(scan[0]) - 1) and (scan[pos[0]][pos[1] + 1] <= height_limit):
        candidates.append((pos[0], pos[1] + 1))
    if (pos[0] > 0) and (scan[pos[0] - 1][pos[1]] <= height_limit):
        candidates.append((pos[0] - 1, pos[1]))
    if (pos[1] > 0) and (scan[pos[0]][pos[1] - 1] <= height_limit):
        candidates.append((pos[0], pos[1] - 1))
    return candidates


def find_shortest_path(scan, start, end):
    queue = deque([start])
    dist = [[-1 for i in range(len(scan[0]))] for j in range(len(scan))]
    dist[start[0]][start[1]] = 0
    while queue:
        curr = queue.pop()
        candidates = get_candidates(curr, scan)
        for cand in candidates:
            if dist[cand[0]][cand[1]] >= 0:
                continue
            else:
                dist[cand[0]][cand[1]] = dist[curr[0]][curr[1]] + 1
            if cand == end:
                return dist[cand[0]][cand[1]]
            queue.appendleft(cand)


def find_best_trail(scan, end):
    shortest_path = None
    for i, line in enumerate(scan):
        for j, height in enumerate(line):
            if height > 0:
                continue
            cand = find_shortest_path(scan, (i, j), end)
            if cand is None:
                continue
            if (shortest_path is None) or (cand < shortest_path):
                shortest_path = cand
    return shortest_path


def main():
    data = data_folder.joinpath("input.txt").read_text()
    scan, start, end = parse_data(data)

    print("Part 1")
    shortest_path = find_shortest_path(scan, start, end)
    print(f"The shortest path from the start has length {shortest_path}.")
    print()

    print("Part 2")
    shortest_path = find_best_trail(scan, end)
    print(f"The shortest path from any start with elevation a has length {shortest_path}.")
    print()


if __name__ == "__main__":
    main()
