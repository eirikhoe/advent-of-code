from hashlib import md5
from math import gcd
import re
from pathlib import Path


def find_delay(data):
    reg = re.compile(
        "Disc #(\d+) has (\d+) positions; at time=0, it is at position (\d+)."
    )
    disks = []
    for line in data.split("\n"):
        m = reg.match(line)
        disks.append((int(m.group(2)), int(m.group(3))))

    a = disks[0][1]
    b = disks[0][0]
    delay = (b - ((a + 1) % b)) % b
    g = b
    for i in range(2, len(disks) + 1):
        a = disks[i - 1][1]
        b = disks[i - 1][0]
        k = (a + i + delay) % b
        m = 0
        while (k > 0) and ((m * g % b) != b - k):
            m += 1
        delay += m * g
        g = g * b // gcd(g, b)

    return delay


def main():
    data_folder = Path(".").resolve()
    print("Part 1")
    data = data_folder.joinpath("input_1.txt").read_text()
    print(
        f"Waiting {find_delay(data)} seconds is the minimum wait that gets you a capsule"
    )
    print()

    print("Part 2")
    data = data_folder.joinpath("input_2.txt").read_text()
    print(
        f"Waiting {find_delay(data)} seconds is the minimum wait that gets you a capsule"
    )


if __name__ == "__main__":
    main()
