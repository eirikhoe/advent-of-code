from pathlib import Path
from collections import defaultdict

data_folder = Path(".").resolve()

number_path_dict = dict()
string_numbers = [
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]
num = 1
for s in string_numbers:
    if s[0] not in number_path_dict:
        number_path_dict[s[0]] = dict()
    curr_dict = number_path_dict[s[0]]
    for c in s[1:-1]:
        curr_dict[c] = dict()
        curr_dict = curr_dict[c]
    curr_dict[s[-1]] = str(num)
    num += 1


def parse_data(data):
    data = [list(char) for char in data.split("\n")]
    return data


def extract_numbers(line, include_text):
    numbers = []
    for i, c in enumerate(line):
        try:
            int(c)
            numbers.append(c)
            continue
        except ValueError:
            pass
        if not include_text:
            continue
        j = i
        curr_dict = number_path_dict
        val = None
        while True:
            if (j < len(line)) and (line[j] in curr_dict):
                curr_dict = curr_dict[line[j]]
                j += 1
            else:
                break
            try:
                int(curr_dict)
                val = curr_dict
                break
            except TypeError:
                continue
        if val is not None:
            numbers.append(val)
    return numbers


def find_calibration_value(line, include_text):
    integers = extract_numbers(line, include_text)
    first_integer = integers[0]
    last_integer = integers[-1]
    calibration_value = int(first_integer + last_integer)
    return calibration_value


def find_calibration_sum(document, include_text):
    return sum([find_calibration_value(line, include_text) for line in document])


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    document = parse_data(data)

    print("Part 1")
    calibration_sum = find_calibration_sum(document, include_text=False)
    print(f"The sum of the calibration values is {calibration_sum}")
    print()

    print("Part 2")
    calibration_sum = find_calibration_sum(document, include_text=True)
    print(
        "The sum of the calibration values when including numbers spelled"
        f" out with letters is {calibration_sum}"
    )
    print()


if __name__ == "__main__":
    main()
