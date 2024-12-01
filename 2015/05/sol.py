from pathlib import Path

data_folder = Path(".").resolve()


def is_string_nice(string):
    vowels = list("aeiou")
    naughty_string = ["ab", "cd", "pq", "xy"]
    vowel_count = 0
    repeat_char = False
    for i, char in enumerate(string[:-1]):
        vowel_count += int(char in vowels)
        if string[i] == string[i + 1]:
            repeat_char = True
        if string[i : i + 2] in naughty_string:
            return False
    vowel_count += int(string[-1] in vowels)
    if (vowel_count >= 3) and repeat_char:
        return True
    else:
        return False


def is_string_nice_improved(string):
    pairs = set()
    previous_pair = None
    repeat_char = False
    repeat_pair = False
    for i, char in enumerate(string[:-1]):
        if (i < (len(string) - 2)) and (string[i] == string[i + 2]):
            repeat_char = True
        pair = string[i : i + 2]
        if pair in pairs:
            repeat_pair = True
        if previous_pair is not None:
            pairs.add(previous_pair)
        previous_pair = pair
        if repeat_pair and repeat_char:
            return True
    return False


def count_nice_strings(data, improved=False):
    n_nice_strings = 0
    if improved:
        count_func = is_string_nice_improved
    else:
        count_func = is_string_nice
    for line in data.split("\n"):
        n_nice_strings += int(count_func(line))
    return n_nice_strings


def main():
    data = data_folder.joinpath("input.txt").read_text()
    print("Part 1")
    print(f"{count_nice_strings(data)} strings are nice")
    print()

    print("Part 2")
    print(f"{count_nice_strings(data,True)} strings are nice using the improved model")


if __name__ == "__main__":
    main()
