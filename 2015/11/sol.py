def find_legal_password(old_password):
    legal = False
    candidate = old_password
    while not legal:
        candidate = increment(candidate)
        legal = legal_password(candidate)
    return candidate


def increment(string):
    remainder = 1
    index = len(string) - 1
    string_list = list(string)
    while remainder > 0:
        string_int = ord(string_list[index]) - ord("a") + 1
        remainder = string_int // 26
        string_list[index] = chr((string_int % 26) + ord("a"))
        index -= 1
    return "".join(string_list)


def legal_password(string):
    forbidden_chars = list("iol")

    for forbidden_char in forbidden_chars:
        if forbidden_char in string:
            return False

    increasing_count = 1
    increasing_straight = False
    pair_last = False
    pair_count = 0

    for i, char in enumerate(string[:-1]):
        if ord(string[i + 1]) - ord(string[i]) == 1:
            increasing_count += 1
        else:
            increasing_count = 1
        if increasing_count >= 3:
            increasing_straight = True

        if (not pair_last) and (string[i] == string[i + 1]):
            pair_count += 1
            pair_last = True
        else:
            pair_last = False

    return (pair_count >= 2) and increasing_straight


def main():
    curr_password = "hepxcrrq"
    print("Part 1")
    new_password = find_legal_password(curr_password)
    print(f"His next password after {curr_password} should be {new_password}")
    print()

    print("Part 2")
    new_new_password = find_legal_password(new_password)
    print(f"His next password after {new_password} should be {new_new_password}")


if __name__ == "__main__":
    main()
