from pathlib import Path

data_folder = Path(".").resolve()


def main():
    data = data_folder.joinpath("input.txt").read_text()
    digits = [int(d) for d in data]
    n_digits = len(digits)

    print("Part 1")
    print(f"The inverse captcha solution is {match_sum(digits,1,n_digits)}")
    print()

    print("Part 2")
    print(f"The inverse captcha solution is {match_sum(digits,n_digits//2,n_digits)}")


def match_sum(digits, gap, n_digits):
    sum_match = 0
    for i in range(n_digits - 1):
        if digits[i] == digits[(i + gap) % n_digits]:
            sum_match += digits[i]
    return sum_match


if __name__ == "__main__":
    main()
