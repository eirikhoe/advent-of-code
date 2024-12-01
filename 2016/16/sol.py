from hashlib import md5
from collections import deque


def gen_data(salt, disk_size):
    data = [int(d) for d in salt]
    while len(data) < disk_size:
        new_data = [1 - d for d in data[::-1]]
        data = data + [0] + new_data

    data = data[:disk_size]
    return data


def compute_checksum(data):
    data = data.copy()
    while (len(data) % 2) == 0:
        checksum = []
        for i in range(0, len(data), 2):
            checksum.append(int(data[i] == data[i + 1]))
        data = checksum
    return "".join([str(d) for d in checksum])


def main():
    salt = "01000100010010111"

    print("Part 1")
    disk_size = 272
    data = gen_data(salt, disk_size)
    print(
        f"The correct checksum with disk size {disk_size} is {compute_checksum(data)}"
    )
    print()

    print("Part 2")
    disk_size = 35651584
    data = gen_data(salt, disk_size)
    print(
        f"The correct checksum with disk size {disk_size} is {compute_checksum(data)}"
    )


if __name__ == "__main__":
    main()
