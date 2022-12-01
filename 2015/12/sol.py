from pathlib import Path
import re

data_folder = Path(__file__).parent.resolve()
reg_num = re.compile(r"(-?\d+)")
reg_obj_red = re.compile(r":\"red\"")


def sum_numbers(data, non_red_only=False):
    if non_red_only:
        data = _remove_red(data)
    num_list = reg_num.findall(data)
    num_int_list = [int(d) for d in num_list]
    return sum(num_int_list)


def _remove_red(data):
    m = reg_obj_red.search(data)
    symb = ["{", "}"]
    search_dir = [-1, 1]
    while m is not None:
        indices = list(m.span())
        count = 0
        for i in range(2):
            index = indices[i]
            while (count != 0) or (data[index] != symb[i]):
                if data[index] == "}":
                    count += 1
                elif data[index] == "{":
                    count -= 1
                index += search_dir[i]
            indices[i] = index
        data = data[: indices[0]] + data[(indices[1] + 1) :]
        m = reg_obj_red.search(data)
    return data


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    numbers_sum = sum_numbers(data)

    print("Part 1")
    print(f"The sum of all the numbers in the document is {numbers_sum}")
    print()

    print("Part 2")
    numbers_sum = sum_numbers(data, True)
    print(
        "The sum of all the numbers in the document with red "
        + f"objects removed is {numbers_sum}"
    )


if __name__ == "__main__":
    main()
