from pathlib import Path
import re
from collections import deque

data_folder = Path(".").resolve()
reg = re.compile(r"(\d+): (\d+)")


def severity(layers, delay):
    severity = 0
    for layer in layers:
        if ((delay + layer[0]) % (2 * (layer[1] - 1))) == 0:
            severity += layer[0] * layer[1]
    return severity


def check_if_caught(layers, delay):
    caught = False
    for layer in layers:
        if ((delay + layer[0]) % (2 * (layer[1] - 1))) == 0:
            caught = True
            break
    return caught


def main():
    data = data_folder.joinpath("input.txt").read_text()
    layers = []
    for line in data.split("\n"):
        m = reg.match(line)
        layer_info = [int(m.group(1)), int(m.group(2))]
        layers.append(layer_info)

    print("Part 1")
    delay = 0
    curr_severity = severity(layers, 0)
    print(f"The severity if the packet leaves immediately is {curr_severity}")
    print()
    caught = True
    while caught:
        delay += 1
        caught = check_if_caught(layers, delay)

    print("Part 2")
    print(f"The packet won't get caught if it waits {delay} picoseconds")


if __name__ == "__main__":
    main()
