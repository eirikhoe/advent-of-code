from pathlib import Path
import copy

data_folder = Path(".").resolve()


def parse_data(data):
    formations = [
        [list(line) for line in formation.split("\n")]
        for formation in data.split("\n\n")
    ]

    return formations


def is_equal(first, second):
    return all([first[i] == second[i] for i, _ in enumerate(first)])


def test_equality_row(formation, row):
    n_tests = min(row, len(formation) - row)
    for i in range(n_tests):
        first = formation[row - i - 1]
        second = formation[row + i]
        if not is_equal(first, second):
            return False
    return True


def test_equality_col(formation, col):
    n_tests = min(col, len(formation[0]) - col)
    for i in range(n_tests):
        first = [row[col - i - 1] for row in formation]
        second = [row[col + i] for row in formation]
        if not is_equal(first, second):
            return False
    return True


def find_patterns(formation, ignore=None):
    for i in range(1, len(formation)):
        if test_equality_row(formation, i):
            if (ignore is None) or ((i, 0) != ignore):
                return (i, 0)

    for j in range(1, len(formation[0])):
        if test_equality_col(formation, j):
            if (ignore is None) or ((j, 1) != ignore):
                return (j, 1)
    return None


def reverse(formation, pos):
    if formation[pos[0]][pos[1]] == "#":
        formation[pos[0]][pos[1]] = "."
    else:
        formation[pos[0]][pos[1]] = "#"
    return formation


def find_smudge_pattern(formation, orig_pattern):
    for i, _ in enumerate(formation):
        for j, _ in enumerate(formation[0]):
            fixed = copy.deepcopy(formation)
            fixed = reverse(fixed, (i, j))
            pattern = find_patterns(fixed, orig_pattern)
            if pattern is not None:
                return pattern
    return None


def get_score(pattern):
    score = pattern[0]
    if pattern[1] == 0:
        score *= 100
    return score


def sum_patterns(formations, smudge):
    sum = 0
    for formation in formations:
        pattern = find_patterns(formation)
        if (pattern is not None) and (not smudge):
            sum += get_score(pattern)
        else:
            pattern = find_smudge_pattern(formation, pattern)
            if pattern is not None:
                sum += get_score(pattern)
    return sum


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    formations = parse_data(data)

    print("Part 1")
    print(f"The sum of notes is {sum_patterns(formations,False)}.")
    print()

    print("Part 2")
    print(f"The sum of notes with smudges is {sum_patterns(formations,True)}.")
    print()


if __name__ == "__main__":
    main()
