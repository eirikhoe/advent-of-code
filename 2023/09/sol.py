from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    sequences = [[int(d) for d in line.split()] for line in data.split("\n")]
    return sequences


def diff(sequence):
    return [sequence[i + 1] - sequence[i] for i, _ in enumerate(sequence[1:])]


def predict_next_element(sequence, forward):
    if all([el == 0 for el in sequence]):
        return 0
    diff_seq = diff(sequence)
    next_diff = predict_next_element(diff_seq, forward)
    if forward:
        return sequence[-1] + next_diff
    else:
        return sequence[0] - next_diff


def sum_next_elements(sequences, forward):
    predict = lambda sequence: predict_next_element(sequence, forward)
    return sum(map(predict, sequences))


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    sequences = parse_data(data)

    print("Part 1")
    next_values = sum_next_elements(sequences, True)
    print(f"The sum of extrapolated forward values is {next_values}.")
    print()

    print("Part 2")
    next_values = sum_next_elements(sequences, False)
    print(f"The sum of extrapolated backward values is {next_values}.")
    print()


if __name__ == "__main__":
    main()
