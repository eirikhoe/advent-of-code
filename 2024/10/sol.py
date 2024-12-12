from pathlib import Path
from collections import deque

data_folder = Path(".").resolve()


def parse_data(data):
    top_map = [[int(d) for d in row] for row in data.split("\n")]
    return top_map


def get_candidates(point, top_map):
    size = (len(top_map), len(top_map[0]))
    curr_el = top_map[point[0]][point[1]]
    cands = []
    for j in range(2):
        for d in [-1, 1]:
            cand = list(point)
            cand[j] += d
            if (0 <= cand[j] < size[d]) and (
                top_map[cand[0]][cand[1]] == (curr_el + 1)
            ):
                cands.append(tuple(cand))
    return cands


def score_trailheads(top_map, only_endpoints):
    score = 0
    for i, row in enumerate(top_map):
        for j, el in enumerate(row):
            if el == 0:
                score += score_trailhead((i, j), top_map, only_endpoints)
    return score


def score_trailhead(start, top_map, only_endpoints):
    queue = deque([start])
    trailheads = []
    while len(queue) > 0:
        point = queue.popleft()
        if top_map[point[0]][point[1]] == 9:
            trailheads.append(point)
            continue
        for candidate in get_candidates(point, top_map):
            queue.append(candidate)
    if only_endpoints:
        trailheads = list(set(trailheads))
    return len(trailheads)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    top_map = parse_data(data)

    print("Part 1")
    score = score_trailheads(top_map, only_endpoints=True)
    print(f"The score of all trailheads is {score}.")
    print()

    print("Part 2")
    rating = score_trailheads(top_map, only_endpoints=False)
    print(f"The rating of all trailheads is {rating}.")
    print()


if __name__ == "__main__":
    main()
