from pathlib import Path
import re
from collections import deque
import math
from copy import deepcopy

line_reg = re.compile(r"Blueprint \d+:(.+)")
cost_reg = re.compile(r"Each (\w+) robot costs ((?:\d+ \w+(?:\.| and ))+)")


data_folder = Path(".").resolve()


def parse_data(data):
    blueprints = []
    for line in data.split("\n"):
        g = line_reg.match(line).groups()
        cost_info = g[0]
        blueprint_costs = dict()
        for costs in cost_reg.findall(cost_info):
            robot_costs = dict()
            for cost in costs[1].rstrip(".").split(" and "):
                amount, resource = cost.split()
                amount = int(amount)
                robot_costs[resource] = amount
            blueprint_costs[costs[0]] = robot_costs
        blueprints.append(blueprint_costs)
    return blueprints


def can_afford(robot, resources):
    enough = True
    for resource, amount in robot.items():
        if resources[resource] < amount:
            enough = False
            break
    return enough


def _get_candidates(blueprint, resources, robots):
    new_resources = deepcopy(resources)
    for robot, amount in robots.items():
        new_resources[robot] += amount
    cands = []

    for type, robot in blueprint.items():
        if not can_afford(robot, resources):
            continue
        curr_resources = deepcopy(new_resources)
        curr_robots = deepcopy(robots)
        for resource, amount in robot.items():
            curr_resources[resource] -= amount
        curr_robots[type] += 1
        cands.append((curr_robots, curr_resources))
    if len(cands) < len(blueprint):
        cands.append((deepcopy(robots), deepcopy(new_resources)))
    return cands


MATERIALS = ["ore", "clay", "obsidian", "geode"]


def make_state(robots, resources, time, time_limit):
    res = []
    rob = []
    for material in MATERIALS:
        rob.append(robots[material])
        res.append(resources[material])
    low_lim, high_lim = find_limits(robots, resources, time, time_limit)
    return (tuple(rob), tuple(res), time, low_lim, high_lim)


def find_limits(robots, resources, time, time_limit):
    rem_time = time_limit - time
    min_lim = resources["geode"] + robots["geode"] * rem_time
    max_lim = resources["geode"] + int(
        (robots["geode"] + (rem_time - 1) / 2) * rem_time
    )
    return min_lim, max_lim


def find_optimal_geode_amounts(blueprints, time_limit):
    optimal_geodes = []
    for blueprint in blueprints:
        n_geode = find_optimal_geode_amount(blueprint, time_limit)
        optimal_geodes.append(n_geode)
    return optimal_geodes


def make_seen_key(state):
    rob, res, _, _, _ = state
    return (rob[:-1], res[:-1])


def check_end_state(blueprint, robots):
    end_state = True
    for material in blueprint["geode"]:
        if blueprint["geode"][material] > robots[material]:
            end_state = False
            break
    return end_state


def find_optimal_geode_amount(blueprint, time_limit):
    resources = dict()
    robots = dict()
    for material in MATERIALS:
        resources[material] = 0
        robots[material] = 0
    robots["ore"] = 1
    state = make_state(robots, resources, 0, time_limit)
    seen = dict()
    seen[make_seen_key(state)] = state[3]
    intermediates = deque([state])

    best = 0
    while len(intermediates) > 0:
        state = intermediates.pop()
        rob, res, time, low_lim, high_lim = state
        for i, material in enumerate(MATERIALS):
            resources[material] = res[i]
            robots[material] = rob[i]
        if high_lim <= best:
            continue
        if check_end_state(blueprint, robots) and (high_lim > best):
            best = high_lim
        if low_lim > best:
            best = low_lim
        for robot_cand, resources_cand in _get_candidates(blueprint, resources, robots):
            state = make_state(robot_cand, resources_cand, time + 1, time_limit)
            seen_state = make_seen_key(state)
            if (not seen_state in seen) or (seen[seen_state] < state[3]):
                seen[seen_state] = state[3]
                intermediates.appendleft(state)

    return best


def main():
    data = data_folder.joinpath("input.txt").read_text()
    blueprints = parse_data(data)

    print("Part 1")
    geode_amounts = find_optimal_geode_amounts(blueprints, 24)
    quality_level_sum = 0
    for id, amount in enumerate(geode_amounts):
        quality_level_sum += (id + 1) * amount
    print(
        f"The sum of the quality levels for all the blueprints in the list is {quality_level_sum}."
    )
    print()

    print("Part 2")
    geode_amounts = find_optimal_geode_amounts(blueprints[:3], 32)
    print(
        f"The product of the optimal geode amounts for the first three blueprints is {math.prod(geode_amounts)}."
    )
    print()


if __name__ == "__main__":
    main()
