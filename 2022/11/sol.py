from pathlib import Path
import re
import math
from copy import deepcopy

data_folder = Path(".").resolve()

monkey_reg = re.compile(
    r"\s*Monkey (\d):\s+Starting items:((?: \d+,?)+)\s+Operation: new = (.+)"
    + r"\s+Test: divisible by (\d+)\s+If true: throw to monkey (\d)"
    + r"\s+If false: throw to monkey (\d)",
    flags=re.MULTILINE,
)


class Monkey:
    def __init__(self, description: str) -> None:
        info = monkey_reg.match(description).groups()
        self.id = int(info[0])
        self.items = [int(item) for item in info[1].strip().split(", ")]
        self.eq_str = info[2].strip()
        self.worry_level_eq = lambda old: eval(self.eq_str)
        self.mod = int(info[3])
        self.give_to_if_true = int(info[4])
        self.give_to_if_false = int(info[5])
        self.n_inspections = 0


def inspect_and_test(monkey, manageable_worry, max_mod=None):
    worry_level = monkey.items.pop(0)
    worry_level = monkey.worry_level_eq(worry_level)
    if manageable_worry:
        worry_level = worry_level // 3
    else:
        worry_level %= max_mod
    if worry_level % monkey.mod == 0:
        give_to = monkey.give_to_if_true
    else:
        give_to = monkey.give_to_if_false
    return worry_level, give_to


def do_round(monkeys, manageable_worry, max_mod):
    for monkey in monkeys:
        while len(monkey.items) > 0:
            monkey.n_inspections += 1
            worry_level, give_to = inspect_and_test(monkey, manageable_worry, max_mod)
            monkeys[give_to].items.append(worry_level)


def do_rounds(monkeys, n_rounds, manageable_worry):
    max_mod = math.prod([monkey.mod for monkey in monkeys])
    for _ in range(n_rounds):
        do_round(monkeys, manageable_worry, max_mod)


def parse_data(data):
    monkeys = [Monkey(description) for description in data.split("\n\n")]
    return monkeys


def compute_monkey_business(monkeys):
    inspections = sorted([monkey.n_inspections for monkey in monkeys])
    monkey_business = inspections[-2] * inspections[-1]
    return monkey_business


def main():
    data = data_folder.joinpath("input.txt").read_text()
    init_monkeys = parse_data(data)

    print("Part 1")
    monkeys = deepcopy(init_monkeys)
    do_rounds(monkeys, 20, manageable_worry=True)
    monkey_business = compute_monkey_business(monkeys)
    print(f"The monkey business is {monkey_business}")
    print()

    print("Part 2")
    monkeys = deepcopy(init_monkeys)
    do_rounds(monkeys, 10000, manageable_worry=False)
    monkey_business = compute_monkey_business(monkeys)
    print(f"The monkey business is {monkey_business}")
    print()


if __name__ == "__main__":
    main()
