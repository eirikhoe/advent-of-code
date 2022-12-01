from pathlib import Path
from itertools import product


def parse_rules(lines):
    rules = dict()
    i = 0
    for i, line in enumerate(lines):
        if not line:
            break
        j = line.find(":")
        rule = line[j + 1 :]
        rule_index = int("".join(line[:j]))
        if '"' in rule:
            rule = rule.strip(r" \"")
        else:
            elements = rule.split()
            rule = []
            rule.append([])
            for element in elements:
                if element == "|":
                    rule.append([])
                else:
                    rule[-1].append(int(element))
        rules[rule_index] = rule
    return rules, i


def count_valid_messages(rules, messages, loops):
    """
    Assumes the structure of the problem holds. Thus
    rule 0 is made up entirely of rule 42 and 31, see
    _validate for details.
    """
    n_valid = 0
    left_options = find_rule_options(rules, 42)
    left_lengths = [len(l) for l in left_options]
    assert min(*left_lengths) == max(*left_lengths)

    right_options = find_rule_options(rules, 31)
    right_lengths = [len(r) for r in right_options]
    assert min(*right_lengths) == max(*right_lengths)

    for message in messages:
        n_valid += _validate(message, loops, left_options, right_options)
    return n_valid


def find_rule_options(rules, ind):
    if isinstance(rules[ind], str):
        return [rules[ind]]
    res = []
    for rule_part in rules[ind]:
        partial_results = []
        for rule_ind in rule_part:
            partial_result = find_rule_options(rules, rule_ind)
            partial_results.append(partial_result)
        ranges = [range(len(r)) for r in partial_results]
        for combination in product(*ranges):
            result = ""
            for i in range(len(partial_results)):
                result += partial_results[i][combination[i]]
            res.append(result)
    return res


def _validate(message, loops, left_options, right_options):
    """
    Assumes the structure of the problem holds. Thus denoting 
    rules by their number we have that without loops 
    0 = 42 42 31. With loops rule 0 is n 42s followed by
    m 31s where n > m >= 1.
    """
    n = 0
    len_l = len(left_options[0])
    i = 0
    while message[i : i + len_l] in left_options:
        n += 1
        i += len_l

    m = 0
    len_r = len(right_options[0])
    while message[i : i + len_r] in right_options:
        m += 1
        i += len_r
    return (i == len(message)) and (n > m >= 1) and (loops or (n + m == 3))


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    lines = data.split("\n")
    rules, i = parse_rules(lines)
    messages = lines[i + 1 :]

    print("Part 1")
    n_valid = count_valid_messages(rules, messages, loops=False)
    print(f"Without loops {n_valid} messages completely match rule 0")
    print()

    print("Part 2")
    n_valid = count_valid_messages(rules, messages, loops=True)
    print(f"With loops {n_valid} messages completely match rule 0")


if __name__ == "__main__":
    main()
