from pathlib import Path
from collections import defaultdict
import copy

data_folder = Path(".").resolve()


def parse_data(data):
    hands = [line.split() for line in data.split("\n")]
    for i, _ in enumerate(hands):
        hands[i][1] = int(hands[i][1])
    return hands


def get_count(cards, include_jokers):
    count = defaultdict(int)
    for card in cards:
        count[card] += 1
    n_jokers = 0
    if include_jokers and (0 in count):
        if len(count) == 1:
            return [5]
        n_jokers = count.pop(0)
    count = sorted([val for _, val in count.items()], reverse=True)
    if include_jokers:
        count[0] += n_jokers
    return count


def determine_value(count):
    if count[0] >= 4:
        return 1 + count[0]
    elif count[0] >= 2:
        return 3 + count[0] - len(count)
    else:
        return 0


def compare_hands(hand, include_jokers):
    cards = hand[0]
    value = determine_value(get_count(cards, include_jokers))
    value *= 13**5
    for i, card in enumerate(cards):
        value += card * (13 ** (4 - i))
    return value


def find_total_winnings(hands, include_jokers=False):
    hands = copy.deepcopy(hands)
    values = dict(zip("23456789TJQKA", list(range(13))))
    if include_jokers:
        values = dict(zip("J23456789TQKA", list(range(13))))
    for i, _ in enumerate(hands):
        hands[i][0] = tuple(values[card] for card in hands[i][0])
    key_func = lambda hand: compare_hands(hand, include_jokers)
    hands = sorted(hands, key=key_func)
    winnings = 0
    for i, _ in enumerate(hands):
        winnings += (i + 1) * hands[i][1]
    return winnings


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    hands = parse_data(data)

    print("Part 1")
    total_winnings = find_total_winnings(hands, include_jokers=False)
    print(f"The total winnings without jokers is {total_winnings}.")
    print()

    print("Part 2")
    total_winnings = find_total_winnings(hands, include_jokers=True)
    print(f"The total winnings with jokers is {total_winnings}.")
    print()


if __name__ == "__main__":
    main()
