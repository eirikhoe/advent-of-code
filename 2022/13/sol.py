from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    pairs = [[eval(l) for l in pair.split("\n")] for pair in data.split("\n\n")]
    return pairs


def base_compare(left, right):
    if left < right:
        return 1
    elif right < left:
        return -1
    else:
        return 0


def check_order(left, right):
    if isinstance(left, int) and isinstance(right, int):
        return base_compare(left, right)
    elif isinstance(left, list) and isinstance(right, list):
        l_len = len(left)
        r_len = len(right)
        for i in range(min(r_len, l_len)):
            order = check_order(left[i], right[i])
            if order != 0:
                return order
        return base_compare(l_len, r_len)
    elif isinstance(left, int):
        return check_order([left], right)
    else:
        return check_order(left, [right])


def find_right_order_indicies_sum(pairs):
    index_sum = 0
    for i, pair in enumerate(pairs):
        if check_order(pair[0], pair[1]) == 1:
            index_sum += i + 1
    return index_sum


def bubble_sort(items):
    sorted = False
    while not sorted:
        sorted = True
        for i in range(len(items) - 1):
            if check_order(items[i], items[i + 1]) == -1:
                items[i], items[i + 1] = items[i + 1], items[i]
                sorted = False
    return items


def find_decoder_key(pairs):
    key_items = [[[2]], [[6]]]
    items = []
    items.extend(key_items)
    for pair in pairs:
        items.extend(pair)
    items = bubble_sort(items)
    decoder_key = 1
    for i, item in enumerate(items):
        if item in key_items:
            decoder_key *= i + 1
    return decoder_key


def main():
    data = data_folder.joinpath("input.txt").read_text()
    pairs = parse_data(data)

    print("Part 1")
    right_index_sum = find_right_order_indicies_sum(pairs)
    print(f"The indicies of the pairs in right order have sum {right_index_sum}.")
    print()

    print("Part 2")
    decoder_key = find_decoder_key(pairs)
    print(f"The decoder key is {decoder_key}.")


if __name__ == "__main__":
    main()
