from pathlib import Path
from collections import defaultdict

data_folder = Path(".").resolve()

MATCHING = {
    "(": ")",
    "[": "]",
    "{": "}",
    "<": ">",
}
SYNTAX_ERROR_POINTS = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}
AUTOCOMPLETE_POINTS = {
    ")": 1,
    "]": 2,
    "}": 3,
    ">": 4,
}


def parse_data(data):
    return [line for line in data.split("\n")]


def score_lines(lines):
    total_syntax_error_score = 0
    autocomplete_scores = []
    for line in lines:
        seen_pars = []
        autocomplete_score = 0
        for bracket in line:
            if bracket in MATCHING:
                seen_pars.append(bracket)
            elif bracket == MATCHING[seen_pars[-1]]:
                seen_pars.pop()
            else:
                total_syntax_error_score += SYNTAX_ERROR_POINTS[bracket]
                seen_pars = []
                break
        for rem_pars in reversed(seen_pars):
            autocomplete_score *= 5
            autocomplete_score += AUTOCOMPLETE_POINTS[MATCHING[rem_pars]]
        if autocomplete_score > 0:
            autocomplete_scores.append(autocomplete_score)
    autocomplete_scores.sort()
    winning_autocomplete_score = autocomplete_scores[len(autocomplete_scores) // 2]
    return total_syntax_error_score, winning_autocomplete_score


def main():
    data = data_folder.joinpath("input.txt").read_text()
    lines = parse_data(data)
    total_syntax_error_score, winning_autocomplete_score = score_lines(lines)

    print("Part 1")
    print(f"The total syntax error score is {total_syntax_error_score}")
    print()

    print("Part 2")
    print(f"The winning autocomplete score is {winning_autocomplete_score}")
    print()


if __name__ == "__main__":
    main()
