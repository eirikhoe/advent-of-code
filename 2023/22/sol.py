from pathlib import Path
import copy

data_folder = Path(".").resolve()


def parse_data(data):
    blocks = []
    for line in data.split("\n"):
        block = [tuple(int(d) for d in point.split(",")) for point in line.split("~")]
        blocks.append(block)
    return blocks


def does_intersect(first, second, include_z=True):
    end = 2 + int(include_z)
    for i in range(end):
        if (first[0][i] > second[1][i]) or (second[0][i] > first[1][i]):
            return False
    return True


def check_intersection(blocks, index):
    intersects_with = []
    for i, other in enumerate(blocks):
        if i == index:
            continue
        if does_intersect(blocks[index], other):
            intersects_with.append(i)
    return intersects_with


def move(block, direction):
    block = copy.deepcopy(block)
    for i in range(2):
        block[i] = (block[i][0], block[i][1], block[i][2] + direction)
    return block


def find_supported(blocks):
    supports = []
    supported = [set() for _ in blocks]
    blocks = copy.deepcopy(blocks)
    for i, block in enumerate(blocks):
        moved_block = move(block, 1)
        blocks[i] = moved_block
        supports.append(check_intersection(blocks, i))
        for j in supports[i]:
            supported[j].add(i)
        if block[0][2] == 1:
            supported[i].add(-1)

        blocks[i] = block

    sole_supports = []
    for i, _ in enumerate(supports):
        sole_supports.append([j for j in supports[i] if (len(supported[j]) == 1)])
    return sole_supports, supported


def find_reaction_size(supported, index):
    supported = copy.deepcopy(supported)
    remove = set([index])
    removed = set([index])
    while len(remove) > 0:
        new_remove = set()
        for i, _ in enumerate(supported):
            if i in removed:
                continue
            supported[i] -= remove
            if len(supported[i]) == 0:
                new_remove.add(i)
        remove = new_remove
        removed = removed.union(remove)
    return len(removed) - 1


def find_total_reaction_size(blocks):
    _, supported_start = find_supported(blocks)
    reaction_size_fun = lambda x: find_reaction_size(supported_start, x)
    return sum(map(reaction_size_fun, range(len(blocks))))


def find_breakable(blocks):
    sole_supports, _ = find_supported(blocks)
    n_breakable = len([unit for unit in sole_supports if (len(unit) == 0)])
    return n_breakable


def find_ground_height(block, fallen):
    ground_height = 0
    for other in fallen:
        if does_intersect(other, block, include_z=False):
            ground_height = max(ground_height, other[1][2])
    return ground_height


def fall(blocks):
    blocks = copy.deepcopy(blocks)
    blocks = sorted(blocks, key=lambda x: x[0][2])
    for i, block in enumerate(blocks):
        ground_height = find_ground_height(block, blocks[:i])
        fall_distance = block[0][2] - ground_height - 1
        blocks[i] = move(block, -fall_distance)
    return blocks


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    blocks = parse_data(data)

    print("Part 1")
    fallen_blocks = fall(blocks)
    n_breakable = find_breakable(fallen_blocks)
    print(f"There are {n_breakable} breakable blocks.")
    print()

    print("Part 2")
    reaction_sum = find_total_reaction_size(fallen_blocks)
    print(f"The sum of the reaction sizes is {reaction_sum}.")
    print()


if __name__ == "__main__":
    main()
