from pathlib import Path
import copy

data_folder = Path(".").resolve()


def parse_data(data):
    workflows = dict()
    workflows_str, ratings = data.split("\n\n")
    for workflow in workflows_str.split("\n"):
        name, rules_list = workflow.split("{")
        rules_list = rules_list[:-1].split(",")
        rules_list[:-1] = [rule.split(":") for rule in rules_list[:-1]]
        workflows[name] = rules_list

    ratings = ratings.split("\n")
    for i, rating in enumerate(ratings):
        ratings[i] = rating[1:-1].split(",")
        rating_dict = dict()
        for j, _ in enumerate(ratings[i]):
            name, rating = ratings[i][j].split("=")
            rating = int(rating)
            rating_dict[name] = rating
        ratings[i] = rating_dict
    return workflows, ratings


def check_rule(rating, rule):
    name = rule[0]
    operator = rule[1]
    limit = int(rule[2:])
    if operator == "<":
        return rating[name] < limit
    elif operator == ">":
        return rating[name] > limit
    else:
        raise RuntimeError("Unknown operator")


def parse_workflow(rating, workflow):
    for rule in workflow[:-1]:
        if check_rule(rating, rule[0]):
            return rule[1]
    return workflow[-1]


def is_accepted(rating, workflows):
    workflow_name = "in"
    while workflow_name not in ["A", "R"]:
        workflow_name = parse_workflow(rating, workflows[workflow_name])
    return workflow_name == "A"


def sum_accepted_part_ratings(ratings, workflows):
    return sum(
        sum([values for _, values in rating.items()])
        for rating in ratings
        if is_accepted(rating, workflows)
    )


def merge_intervals(first, second):
    first_ind = 0
    second_ind = 0
    merged = []
    while (first_ind < len(first)) or (second_ind < len(second)):
        if second_ind == len(second):
            curr = first[first_ind]
            first_ind += 1
        elif first_ind == len(first):
            curr = second[second_ind]
            second_ind += 1
        elif first[first_ind][0] <= second[second_ind][0]:
            curr = first[first_ind]
            first_ind += 1
        else:
            curr = second[second_ind]
            second_ind += 1
        if len(merged) == 0:
            merged = [curr]
            continue
        if curr[0] <= merged[-1][1] + 1:
            merged[-1] = [merged[-1][0], max(curr[1], merged[-1][1])]
        else:
            merged.append(curr)
    return merged


def make_full_ranges():
    ranges = dict()
    for char in "xmas":
        ranges[char] = [[1, 4000]]
    return ranges


def check_rule_range(ranges, rule):
    name = rule[0]
    operator = rule[1]
    limit = int(rule[2:])
    passing = copy.deepcopy(ranges)
    fail = copy.deepcopy(ranges)
    if operator == "<":
        for i, range in enumerate(ranges[name]):
            if range[0] >= limit:
                passing[name] = ranges[name][:i]
                fail[name] = ranges[i:]
                break
            elif range[1] >= limit:
                passing[name] = ranges[name][: i + 1]
                passing[name][-1] = [range[0], limit - 1]
                fail[name] = [[limit, range[1]]]
                fail[name].extend(ranges[name][i + 1 :])
                break
    elif operator == ">":
        n = len(ranges[name])
        for i, range in enumerate(ranges[name][::-1]):
            if range[1] <= limit:
                passing[name] = ranges[name][n - i :]
                fail[name] = ranges[name][: n - i]
                break
            elif range[0] <= limit:
                passing[name] = ranges[name][n - i - 1 :]
                passing[name][0] = [limit + 1, range[1]]
                fail[name] = ranges[name][: n - i]
                fail[name][-1] = [range[0], limit]
    else:
        raise RuntimeError("Unknown operator")
    return passing, fail


def get_size_ranges(ranges):
    size = 1
    for _, var_ranges in ranges.items():
        var_size = 0
        for var_range in var_ranges:
            var_size += var_range[1] - var_range[0] + 1
        size *= var_size
    return size


def count_valid_combinations(curr_ranges, name, workflows, level=0):
    if name == "R":
        return 0
    elif name == "A":
        return get_size_ranges(curr_ranges)
    fail = curr_ranges
    count = 0
    for rule in workflows[name][:-1]:
        passing, fail = check_rule_range(fail, rule[0])
        count += count_valid_combinations(passing, rule[1], workflows, level + 1)
    count += count_valid_combinations(fail, workflows[name][-1], workflows, level + 1)
    return count


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    workflows, ratings = parse_data(data)
    print("Part 1")
    sum_part_ratings = sum_accepted_part_ratings(ratings, workflows)
    print(f"The sum of the ratings of the accepted parts is {sum_part_ratings}.")
    print()

    print("Part 2")
    valid_combinations = count_valid_combinations(make_full_ranges(), "in", workflows)
    print(f"{valid_combinations} combinations of ratings would be accepted.")

    print()


if __name__ == "__main__":
    main()
