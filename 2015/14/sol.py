from pathlib import Path
import re

data_folder = Path(__file__).parent.resolve()
reg = re.compile(
    r"(\w+) can fly (\d+) km/s for (\d+) seconds, but then must rest for (\d+) seconds."
)


class Reindeer:
    def __init__(self, data):
        self.name = data[0]
        self.speed = int(data[1])
        self.stamina = int(data[2])
        self.rest = int(data[3])
        self.distance = 0
        self.points = 0

    def get_movement(self, t):
        index = t % (self.stamina + self.rest)
        if index < self.stamina:
            return self.speed
        else:
            return 0


class Race:
    def __init__(self, data):
        self.reindeer = []
        for line in data.split("\n"):
            m = reg.match(line)
            assert m is not None
            self.reindeer.append(Reindeer(m.groups()))

    def race_for(self, t):
        for i in range(t):
            for reindeer in self.reindeer:
                reindeer.distance += reindeer.get_movement(i)

            max_distance = 0
            for reindeer in self.reindeer:
                if reindeer.distance > max_distance:
                    max_distance = reindeer.distance

            for reindeer in self.reindeer:
                if reindeer.distance == max_distance:
                    reindeer.points += 1

        return max_distance

    def get_max_points(self):
        max_points = 0
        for reindeer in self.reindeer:
            if reindeer.points > max_points:
                max_points = reindeer.points
        return max_points


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    r = Race(data)
    t = 2503
    dist = r.race_for(t)
    print("Part 1")
    print("The winning reindeer has traveled " + f"{dist} km after {t} seconds")
    print()
    print("Part 2")
    print(
        "The winning reindeer has " + f"{r.get_max_points()} points after {t} seconds"
    )


if __name__ == "__main__":
    main()
