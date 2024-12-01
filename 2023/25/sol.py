from pathlib import Path
from collections import defaultdict, deque, Counter
import copy


data_folder = Path(".").resolve()


def parse_data(data):
    diagram = defaultdict(list)
    components = set()
    for line in data.split("\n"):
        source, value = line.split(": ")
        destinations = value.split()
        diagram[source].extend(destinations)
        components.add(source)
        components = components.union(set(destinations))
        for destination in destinations:
            diagram[destination].append(source)
    return diagram, list(components)


def find_n_connections(diagram, groups):
    n_connections = 0
    all = set.union(*groups)
    for source in diagram:
        for dest in diagram[source]:
            if (dest not in all) or (source not in all):
                continue
            if any(
                ((source in groups[i]) and (dest in groups[1 - i])) for i in range(2)
            ):
                n_connections += 1
    return n_connections


def cut_wires(diagram, wires):
    for wire in wires:
        for i in range(2):
            diagram[wire[i]].remove(wire[1 - i])
    return diagram


def get_group_size_product(diagram, components):
    count = all_shortest(diagram, components)
    candidates = [c[0] for c in count.most_common()]
    n_wires = len(candidates)
    n_components = len(components)
    for rank_lim in range(3, 3 * n_wires - 5):
        upper = min(rank_lim, n_wires)
        for i in range(0, upper - 2):
            for j in range(i + 1, upper - 1):
                k = rank_lim - i - j
                if k <= j:
                    continue
                wires = [candidates[p] for p in (i, j, k)]
                cut_diagram = cut_wires(copy.deepcopy(diagram), wires)
                shortest_paths = shortest_path(cut_diagram, components[0])
                group_size = len(shortest_paths)
                if group_size < n_components:
                    return group_size * (n_components - group_size)


def all_shortest(diagram, components):
    all_paths = []
    for component in components:
        shortest_paths = shortest_path(diagram, component)
        for dest in shortest_paths:
            all_paths.extend(shortest_paths[dest])
    return Counter(all_paths)


def shortest_path(diagram, start):
    search = deque([start])
    shortest_paths = defaultdict(list)
    shortest_paths[start] = []
    while len(search) > 0:
        curr = search.pop()
        for connected in diagram[curr]:
            if connected not in shortest_paths:
                first = min(curr, connected)
                last = max(curr, connected)
                shortest_paths[connected] = shortest_paths[curr] + [(first, last)]
                search.appendleft(connected)
    return shortest_paths


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    diagram, components = parse_data(data)

    print("Part 1")
    group_size_product = get_group_size_product(diagram, components)
    print(f"The product of the two group sizes is {group_size_product}.")
    print()

    print("Part 2")
    print("No part 2.")
    print()


if __name__ == "__main__":
    main()
