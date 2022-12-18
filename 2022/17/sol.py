from pathlib import Path
import time

data_folder = Path(".").resolve()


class Rocks:
    def __init__(self, winds):
        self.winds = winds
        self.tower = set()
        self.chamber_width = 7
        self.height = 0
        self.wind_id = 0
        self.shapes = "-+LIs"

    def reset(self):
        self.tower = set()
        self.height = 0
        self.wind_id = 0

    def get_id(self, shape):
        has_rock = [False for _ in range(self.chamber_width)]
        y = self.height - 1
        id = []
        while y >= 0:
            for i in range(self.chamber_width):
                pos = (y, i)
                is_rock = pos in self.tower
                id.append(is_rock)
                if is_rock and (not has_rock[i]):
                    has_rock[i] = True
            if sum(has_rock) == self.chamber_width:
                break
            y -= 1
        return (tuple(id), self.wind_id, shape)

    def _get_shape(self, rock_id):
        return self.shapes[rock_id % len(self.shapes)]

    def increase_wind_id(self):
        self.wind_id = (self.wind_id + 1) % len(self.winds)

    def _get_wind(self):
        return self.winds[self.wind_id]

    def find_period(self):
        seen = dict()
        rock_id = 0
        shape = self._get_shape(rock_id)
        id = self.get_id(shape)
        heights = []
        while id not in seen:
            seen[id] = (self.height, rock_id)
            heights.append(self.height)
            self.simulate_falling_rock(shape)
            rock_id += 1
            shape = self._get_shape(rock_id)
            id = self.get_id(shape)
        heights.append(self.height)
        heights = [heights[i] - seen[id][0] for i in range(seen[id][1], len(heights))]
        return (*seen[id], rock_id - seen[id][1], heights)

    @staticmethod
    def get_shape_coords(lower_left_coord, shape):
        y = lower_left_coord[0]
        x = lower_left_coord[1]
        if shape == "-":
            all_coords = [(y, x + i) for i in range(4)]
        elif shape == "+":
            all_coords = [(y + 1, x + i) for i in range(3)]
            all_coords.extend([(y, x + 1), (y + 2, x + 1)])
        elif shape == "L":
            all_coords = [(y, x + i) for i in range(3)]
            all_coords.extend([(y + 1, x + 2), (y + 2, x + 2)])
        elif shape == "I":
            all_coords = [(y + i, x) for i in range(4)]
        elif shape == "s":
            all_coords = [(y + i, x + j) for i in range(2) for j in range(2)]
        return all_coords

    def is_valid(self, pos, shape):
        coords = self.get_shape_coords(pos, shape)
        valid = True
        for coord in coords:
            if (
                (coord in self.tower)
                or (not (0 <= coord[1] < self.chamber_width))
                or (coord[0] < 0)
            ):
                valid = False
                break
        return valid

    def simulate_falling_rock(self, shape):
        pos = (self.height + 3, 2)

        while True:
            wind = self._get_wind()
            self.increase_wind_id()
            if wind == "<":
                new_pos = (pos[0], pos[1] - 1)
            elif wind == ">":
                new_pos = (pos[0], pos[1] + 1)
            if self.is_valid(new_pos, shape):
                pos = new_pos
            new_pos = (pos[0] - 1, pos[1])
            if self.is_valid(new_pos, shape):
                pos = new_pos
            else:
                break
        for coord in self.get_shape_coords(pos, shape):
            self.tower.add(coord)
            if coord[0] + 1 > self.height:
                self.height = coord[0] + 1

    def print_tower(self, coords):
        s = ""
        height = self.height
        for coord in coords:
            if coord[0] + 1 > height:
                height = coord[0] + 1

        for j in range(height):
            s += "|"
            for i in range(self.chamber_width):
                coord = (height - 1 - j, i)
                if coord in self.tower:
                    s += "#"
                elif coord in coords:
                    s += "@"
                else:
                    s += "."
            s += "|\n"
        s += "+" + "-" * self.chamber_width + "+\n"
        out_file = data_folder / "output.txt"
        out_file.write_text(s)

    def find_tower_height(self, n_rocks):
        initial_height, offset, period, height_deltas = self.find_period()
        missing = n_rocks - offset
        if missing < 0:
            self.reset()
            return self.simulate_falling_rocks(n_rocks)
        periods_needed = missing // period
        remainder = missing % period
        self.height = initial_height + periods_needed * height_deltas[-1] + height_deltas[remainder]

    def simulate_falling_rocks(self, n_rocks):
        for i in range(n_rocks):
            shape = self._get_shape(i)
            self.simulate_falling_rock(shape)


def main():
    winds = data_folder.joinpath("input.txt").read_text()
    rocks = Rocks(winds)

    print("Part 1")
    n_rocks = 2022
    rocks.find_tower_height(n_rocks)
    print(f"After {n_rocks} rocks have fallen the tower has height {rocks.height}.")
    print()

    print("Part 2")
    rocks.reset()
    n_rocks = 1000000000000
    rocks.find_tower_height(n_rocks)
    print(f"After {n_rocks} rocks have fallen the tower has height {rocks.height}.")
    print()


if __name__ == "__main__":
    main()
