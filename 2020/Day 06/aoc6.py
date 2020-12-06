from pathlib import Path


def count_yes_any(group_answer):
    return len(set.union(*group_answer))


def count_yes_all(group_answer):
    return len(set.intersection(*group_answer))


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    group_answers = [[set(ans) for ans in gr.split("\n")] for gr in data.split("\n\n")]

    print("Part 1")
    total_yes_any = sum([count_yes_any(ans) for ans in group_answers])
    print("The sum of questions to which anyone answered 'yes'")
    print(f"for all groups is {total_yes_any}")
    print()

    print("Part 2")
    total_yes_all = sum([count_yes_all(ans) for ans in group_answers])
    print("The sum of questions to which everyone answered 'yes'")
    print(f"for all groups is {total_yes_all}")


if __name__ == "__main__":
    main()
