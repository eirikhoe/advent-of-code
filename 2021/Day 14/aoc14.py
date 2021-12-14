from pathlib import Path
import bisect
from collections import Counter, defaultdict

data_folder = Path(".").resolve()


def parse_data(data):
    template, rules_data = data.split("\n\n")
    template = template.strip()
    rules = dict()
    for line in rules_data.split("\n"):
        start, end = line.split(" -> ")
        rules[start] = end

    rule_to_rule = defaultdict(list)
    for pattern in rules:
        patterns = ["".join([pattern[0], rules[pattern]]), "".join([rules[pattern], pattern[1]])]
        for new_pattern in patterns:
            if new_pattern in rules:
                rule_to_rule[pattern].append(new_pattern)
    return template, rules, rule_to_rule


def count_grown_polymer_element(template, rules, rule_to_rule, n_steps):
    poly_count = Counter(template)
    rule_hits = defaultdict(int)
    for pattern in rules:
        rule_hits[pattern] = 0
        for i in range(len(template) - 1):
            if (template[i] == pattern[0]) and (template[i + 1] == pattern[1]):
                rule_hits[pattern] += 1
    for _ in range(n_steps):
        poly_count, rule_hits = do_pair_insertion(poly_count, rules, rule_to_rule, rule_hits)
    sorted_elements = poly_count.most_common()
    return sorted_elements[0][1] - sorted_elements[-1][1]


def do_pair_insertion(poly_count, rules, rule_to_rule, rule_hits):
    new_rule_hits = defaultdict(int)
    for pattern in rule_hits:
        poly_count[rules[pattern]] += rule_hits[pattern]
        for new_pattern in rule_to_rule[pattern]:
            new_rule_hits[new_pattern] += rule_hits[pattern]
    return poly_count, new_rule_hits


def main():
    data = data_folder.joinpath("input.txt").read_text()
    template, rules, rule_to_rule = parse_data(data)

    print("Part 1")
    n_steps = 10
    res = count_grown_polymer_element(template, rules, rule_to_rule, n_steps)
    print(f"After {n_steps} steps there are {res} more of the most common")
    print("element than the least common in the polymer")
    print()

    print("Part 2")
    n_steps = 40
    res = count_grown_polymer_element(template, rules, rule_to_rule, n_steps)
    print(f"After {n_steps} steps there are {res} more of the most common")
    print("element than the least common in the polymer")
    print()


if __name__ == "__main__":
    main()
