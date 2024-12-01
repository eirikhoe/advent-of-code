from pathlib import Path
import re

data_folder = Path(".").resolve()
reg = re.compile(r"([a-z]+)([-=])(\d?)")


class Box:
    def __init__(self):
        self.content = []

    def contains(self, label):
        for i, slot in enumerate(self.content):
            if slot[0] == label:
                return True, i
        return False, None

    def __len__(self):
        return len(self.content)

    def __str__(self):
        slots = []
        for slot in self.content:
            slots.append(f"[{slot[0]} {slot[1]}]")
        return " ".join(slots)

    def op(self, op_type, label, lens):
        if op_type == "-":
            self.remove(label)
        elif op_type == "=":
            self.replace(label, lens)

    def remove(self, label):
        is_in, loc = self.contains(label)
        if is_in:
            self.content.pop(loc)

    def replace(self, label, lens):
        is_in, loc = self.contains(label)
        lens = int(lens)
        content = (label, lens)
        if is_in:
            self.content[loc] = content
        else:
            self.content.append(content)

    def get_lens_focusing_power(self, box_number):
        power = 0
        for i, lens in enumerate(self.content):
            power += (box_number + 1) * (i + 1) * lens[1]
        return power


def parse_data(data):
    lines = data.split(",")
    return lines


def hash(string):
    val = 0
    for c in string:
        val += ord(c)
        val *= 17
        val %= 256
    return val


def print_boxes(boxes):
    s = []
    for i, box in enumerate(boxes):
        if len(box) > 0:
            s.append(f"Box {i}: {box}")
    return "\n".join(s)


def run_hashmap(procedure):
    boxes = [Box() for _ in range(256)]
    for step in procedure:
        label, op_type, lens = reg.match(step).groups()
        target = hash(label)
        boxes[target].op(op_type, label, lens)
    return boxes


def sum_focusing_power(boxes):
    box_powers = [box.get_lens_focusing_power(i) for i, box in enumerate(boxes)]
    return sum(box_powers)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    procedure = parse_data(data)

    print("Part 1")
    hash_sum = sum(map(hash, procedure))
    print(
        "The sum of the hash of the steps of the intitialization "
        f"sequence is {hash_sum}."
    )
    print()

    print("Part 2")
    final_boxes = run_hashmap(procedure)
    focusing_power = sum_focusing_power(final_boxes)
    print(f"The total focusing power of the lens configuration is {focusing_power}.")
    print()


if __name__ == "__main__":
    main()
