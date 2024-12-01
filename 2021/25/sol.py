from pathlib import Path
from dataclasses import dataclass
import time

data_folder = Path(".").resolve()


@dataclass
class Seacucumbers:
    herds: list[set[tuple[int]]]
    floor_size: tuple[int]
    n_steps: int = 0

    def _can_move(self, pos):
        return all(pos not in self.herds[i] for i in range(2))

    def step(self, print):
        self.n_steps += 1
        n_moves = 0
        for i, herd in enumerate(self.herds):
            new_herd = set()
            for unit in herd:
                new_unit = list(unit)
                new_unit[i] = (new_unit[i] + 1) % self.floor_size[i]
                new_unit = tuple(new_unit)
                if self._can_move(new_unit):
                    new_herd.add(new_unit)
                    n_moves += 1
                else:
                    new_herd.add(unit)
            self.herds[i] = new_herd
            if print:
                self.print_image()
        return n_moves

    def print_image(self):
        s = f"After {self.n_steps} step{'s' if self.n_steps != 0 else ''}:\n"
        for i in range(self.floor_size[1]):
            for j in range(self.floor_size[0]):
                if (j, i) in self.herds[0]:
                    s += ">"
                elif (j, i) in self.herds[1]:
                    s += "v"
                else:
                    s += "."
            s += "\n"
        data_folder.joinpath(f"floor.txt").write_text(s)
        time.sleep(0.1)

    def move(self, print=False):
        while self.step(print=print) > 0:
            pass


def parse_data(data):
    lines = data.split("\n")
    floor_size = (len(lines[0]), len(lines))
    herds = [set(), set()]
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == "v":
                herds[1].add((j, i))
            elif char == ">":
                herds[0].add((j, i))
    return Seacucumbers(herds=herds, floor_size=floor_size)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    floor = parse_data(data)
    floor.move(print=True)

    print("Part 1")
    print(f"The first step on which no sea cucumbers move is {floor.n_steps}")
    print()


if __name__ == "__main__":
    main()
