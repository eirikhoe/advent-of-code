from pathlib import Path
import bisect

data_folder = Path(".").resolve()


def parse_data(data):
    data = [int(d) for d in data.split(",")]
    return data


def compute_lowest_cost(crab_pos, cost_type):
    min_pos = min(crab_pos)
    max_pos = max(crab_pos)
    n_crabs = len(crab_pos)
    max_d = max_pos - min_pos
    min_cost = n_crabs * _evaluate_cost(max_d, cost_type) + 1
    for pos in range(min_pos, max_pos + 1):
        cost = 0
        for crab in crab_pos:
            dist = abs(crab - pos)
            cost += _evaluate_cost(dist, cost_type)
        if cost < min_cost:
            min_cost = cost
    return min_cost


def _evaluate_cost(dist, cost_type):
    if cost_type == "constant":
        return dist
    elif cost_type == "linear":
        return (dist * (dist + 1)) // 2


def main():
    data = data_folder.joinpath("input.txt").read_text()
    crab_pos = parse_data(data)

    print("Part 1")
    cost_type = "constant"
    fuel_cost = compute_lowest_cost(crab_pos, cost_type)
    print(f"The optimal alignment position has fuel cost {fuel_cost} when the cost is {cost_type}")
    print()

    print("Part 2")
    cost_type = "linear"
    fuel_cost = compute_lowest_cost(crab_pos, cost_type)
    print(f"The optimal alignment position has fuel cost {fuel_cost} when the cost is {cost_type}")
    print()


if __name__ == "__main__":
    main()
