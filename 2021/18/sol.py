from pathlib import Path
from copy import deepcopy

data_folder = Path(".").resolve()


def parse_data(data):
    numbers = [eval(line) for line in data.split("\n")]
    return numbers


def add(left, right):
    res = [deepcopy(left), deepcopy(right)]
    while True:
        res, did_explode = explode(res)
        did_split = False
        if not did_explode:
            res, did_split = split(res)
            if not did_split:
                break
    return res


def find_explode_index(number, index):
    if len(index) == 5:
        return index[:-1]
    if isinstance(number, int):
        return None
    else:
        left = find_explode_index(number[0], index + [0])
        right = find_explode_index(number[1], index + [1])
    if left is not None:
        return left
    if right is not None:
        return right
    return None


def index_number(number, index):
    res = number
    for i in index:
        res = res[i]
    return res


def set_element(lst, index, value):
    if len(index) == 1:
        lst[index[0]] = value
    else:
        set_element(lst[index[0]], index[1:], value)


def find_insert_ind(number, index, dir):
    if dir == "left":
        val = 1
    else:
        val = 0
    j = len(index) - 1 - index[::-1].index(val)
    ind = index[:j] + [1 - val]
    num = index_number(number, ind)
    while True:
        if isinstance(num, int):
            break
        num = num[val]
        ind += [val]
    return ind, num


def find_magnitude(number):
    if isinstance(number, int):
        return number
    else:
        return 3 * find_magnitude(number[0]) + 2 * find_magnitude(number[1])


def explode(number):
    index = find_explode_index(number, [])
    if index is None:
        return number, False
    exploding_pair = index_number(number, index)

    if max(index) == 1:
        left_ind, num = find_insert_ind(number, index, "left")
        set_element(number, left_ind, num + exploding_pair[0])

    if min(index) == 0:
        right_ind, num = find_insert_ind(number, index, "right")
        set_element(number, right_ind, num + exploding_pair[1])
    set_element(number, index, 0)
    return number, True


def split(number):
    index = find_split_index(number, [])
    if index is None:
        return number, False
    split_num = index_number(number, index)
    split_left = split_num // 2
    split_right = (split_num + 1) // 2
    set_element(number, index, [split_left, split_right])
    return number, True


def find_split_index(number, index):
    if isinstance(number, int):
        if number >= 10:
            return index
        else:
            return None
    else:
        left = find_split_index(number[0], index + [0])
        right = find_split_index(number[1], index + [1])
    if left is not None:
        return left
    if right is not None:
        return right
    return None


def find_sum(numbers):
    sum = numbers[0]
    for i in range(1, len(numbers)):
        sum = add(sum, numbers[i])
    return sum


def find_largest_pair_sum(numbers):
    largest = 0
    for i, _ in enumerate(numbers):
        for j, __ in enumerate(numbers):
            if i == j:
                continue
            s = find_magnitude(add(numbers[i], numbers[j]))
            if s > largest:
                largest = s
    return largest


def main():
    data = data_folder.joinpath("input.txt").read_text()
    numbers = parse_data(data)

    print("Part 1")
    total = find_sum(numbers)
    magnitude = find_magnitude(total)
    print(f"The magnitude of the sum of snailfish numbers is {magnitude}")
    print()

    print("Part 2")
    largest_pair = find_largest_pair_sum(numbers)
    print(
        f"The largest magnitude of the sum of any pair of different snailfish numbers is {largest_pair}"
    )
    print()


if __name__ == "__main__":
    main()
