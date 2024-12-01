from pathlib import Path
import re
import math

data_folder = Path(".").resolve()


def parse_data(data):
    reg = re.compile(r"(\w{3}) = \((\w{3}), (\w{3})\)")
    instructions, lines = data.split("\n\n")
    instructions = [int(i == "R") for i in instructions]
    network = dict()
    for line in lines.split("\n"):
        curr, left, right = re.match(reg, line).groups()
        network[curr] = (left, right)
    return instructions, network


def count_times_instructions(start, instructions, network, strict_end):
    curr = start
    count = 0
    instruction_counter = 0
    n_instructions = len(instructions)
    finished = False
    while not finished:
        curr = network[curr][instructions[instruction_counter]]
        count += 1
        instruction_counter = count % n_instructions
        if strict_end:
            finished = curr == "ZZZ"
        else:
            finished = curr[2] == "Z"
    return count, curr


def count_times_instructions_ghost(instructions, network):
    start_nodes = []
    end_nodes = []
    for node in network:
        if node[2] == "A":
            start_nodes.append(node)
        elif node[2] == "Z":
            end_nodes.append(node)
    start_distances = dict()
    for node in start_nodes:
        start_distances[node] = count_times_instructions(
            node, instructions, network, False
        )
    end_distances = dict()
    for node in end_nodes:
        distance, end = count_times_instructions(node, instructions, network, False)
        # assert that each end_node becomes a loop to itself
        assert end == node
        end_distances[node] = distance
    distances = []
    for node, (distance, end) in start_distances.items():
        # assert that the distance from each start node to an end node is
        # the same as the loop distance from that end node
        assert distance == end_distances[end]
        distances.append(distance)

    #answer is the lowest common multiple of all loop distances
    total_distance = math.lcm(*distances)
    return total_distance


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    instructions, network = parse_data(data)

    print("Part 1")
    n_steps, _ = count_times_instructions("AAA", instructions, network, True)
    print(f"{n_steps} steps is required to reach ZZZ.")
    print()

    print("Part 2")
    n_steps = count_times_instructions_ghost(instructions, network)
    print(f"{n_steps} steps is required to only be at nodes ending in Z.")
    print()


if __name__ == "__main__":
    main()
