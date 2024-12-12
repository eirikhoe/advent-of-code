from pathlib import Path
import copy

data_folder = Path(".").resolve()

def parse_data(data):
    rules_str,updates_str = data.split("\n\n")
    rules = [[int(d) for d in rule.split("|")] for rule in rules_str.split("\n")]
    updates = [[int(d) for d in update.split(",")] for update in updates_str.split("\n")]
    return rules,updates

def validate_update(update,rules):
    broken_rule = None
    for rule in rules:
        valid = check_rule(update,rule)
        if not valid:
            broken_rule = rule
            break
    return valid,broken_rule

def check_rule(update,rule):
    try: 
        first = update.index(rule[0])
        second = update.index(rule[1])
    except ValueError:
        return True
    return first < second

def sum_middle_pages(updates,rules,sum_valid):
    middle_page_sum = 0
    for update in updates:
        valid_update,broken_rule = validate_update(update,rules)
        if valid_update != sum_valid:
            continue
        if not valid_update:
            update = fix_update(update,rules,broken_rule)
        l = len(update)
        middle_page_sum += update[l//2]
    return middle_page_sum

def fix_update(update,rules,broken_rule):
    update = copy.deepcopy(update)
    valid = False
    while not valid:
        first = update.index(broken_rule[0])
        second = update.index(broken_rule[1])
        update[second] = broken_rule[0]
        update[first] = broken_rule[1]
        valid,broken_rule = validate_update(update,rules)
    return update


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    rules, updates = parse_data(data)

    print("Part 1")
    middle_page_sum = sum_middle_pages(updates,rules,True)
    print(f"The sum of the correct middle pages is {middle_page_sum}.")
    print()

    print("Part 2")
    middle_page_sum = sum_middle_pages(updates,rules,False)
    print(f"The sum of the fixed middle pages is {middle_page_sum}.")
    print()


if __name__ == "__main__":
    main()
