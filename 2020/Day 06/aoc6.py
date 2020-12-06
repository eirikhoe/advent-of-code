from pathlib import Path


def count_yes_anyone(group_answer):
    return len(group_answer[0].union(*group_answer[1:]))


def count_yes_everyone(group_answer):
    return len(group_answer[0].intersection(*group_answer[1:]))


count_yes = {"any": count_yes_anyone, "all": count_yes_everyone}


def count_total(group_answers, count_type="any"):
    total_yes = 0
    for group_answer in group_answers:
        total_yes += count_yes[count_type](group_answer)
    return total_yes


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    group_answers = [[set(ans) for ans in gr.split("\n")] for gr in data.split("\n\n")]

    print("Part 1")
    print("The sum of questions to which anyone answered 'yes'")
    print(f"for all groups is {count_total(group_answers,'any')}")
    print()

    print("Part 2")
    print("The sum of questions to which everyone answered 'yes'")
    print(f"for all groups is {count_total(group_answers,'all')}")


if __name__ == "__main__":
    main()
