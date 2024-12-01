from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    numbers = []
    winning_numbers = []
    for line in data.split("\n"):
        _, line = line.split(":")
        number_str, winning_number_str = line.split("|")
        numbers.append([int(d) for d in number_str.strip().split()])
        winning_numbers.append([int(d) for d in winning_number_str.strip().split()])
    return numbers, winning_numbers


def _find_hits(numbers, winning_numbers):
    return len(set(numbers).intersection(set(winning_numbers)))


def find_total_points(numbers, winning_numbers):
    total_points = 0
    for i, _ in enumerate(numbers):
        hits = _find_hits(numbers[i], winning_numbers[i])
        if hits > 0:
            total_points += 2 ** (hits - 1)
    return total_points


def find_total_scratchcards(numbers, winning_numbers):
    cards = [1] * len(numbers)
    for i, _ in enumerate(numbers):
        hits = _find_hits(numbers[i], winning_numbers[i])
        for j in range(i + 1, i + 1 + hits):
            cards[j] += cards[i]
    return sum(cards)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    numbers, winning_numbers = parse_data(data)

    print("Part 1")
    total_points = find_total_points(numbers, winning_numbers)
    print(f"The total number of points is {total_points}.")
    print()

    print("Part 2")
    total_scratchcards = find_total_scratchcards(numbers, winning_numbers)
    print(f"The total number of scratchcards is {total_scratchcards}.")
    print()


if __name__ == "__main__":
    main()
