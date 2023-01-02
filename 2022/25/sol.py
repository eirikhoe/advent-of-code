from pathlib import Path

data_folder = Path(".").resolve()


digit_snafu_to_decimal = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
digit_decimal_to_snafu = {d: s for s, d in digit_snafu_to_decimal.items()}
snafu_base = 5


def parse_data(data):
    numbers = data.split("\n")
    return numbers


def snafu_to_decimal(snafu_number):
    decimal_number = 0
    n = len(snafu_number) - 1
    for i, digit in enumerate(snafu_number):
        decimal_digit = digit_snafu_to_decimal[digit]
        decimal_number += (snafu_base ** (n - i)) * decimal_digit
    return decimal_number


def decimal_to_snafu(decimal_number):
    remainder = decimal_number
    snafu_number = []
    while remainder > 0:
        decimal_digit = ((remainder + 2) % snafu_base) - 2
        snafu_digit = digit_decimal_to_snafu[decimal_digit]
        snafu_number.append(snafu_digit)
        remainder = (remainder - decimal_digit) // snafu_base
    return "".join(reversed(snafu_number))


def sum_snafu_numbers(numbers):
    decimal_sum = 0
    for number in numbers:
        decimal_sum += snafu_to_decimal(number)
    return decimal_to_snafu(decimal_sum)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    snafu_numbers = parse_data(data)

    print("Part 1")
    snafu_sum = sum_snafu_numbers(snafu_numbers)
    print(f"The sum of the SNAFU numbers is {snafu_sum} in SNAFU.")
    print()

    print("Part 2")
    print("Nothing to solve")
    print()


if __name__ == "__main__":
    main()
