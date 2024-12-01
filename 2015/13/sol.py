from pathlib import Path
import numpy as np
import copy
from itertools import permutations
import re

data_folder = Path(__file__).parent.resolve()
reg = re.compile(
    r"(\w+) would (lose|gain) (\d+) happiness units by sitting next to (\w+)."
)


class Table:
    def __init__(self, data):
        happiness = []
        people = set()
        for line in data.split("\n"):
            m = reg.match(line)
            assert m is not None
            new_data = list(m.groups())
            new_data[2] = int(new_data[2])
            if new_data[1] == "lose":
                new_data[2] *= -1
            new_data.pop(1)
            happiness.append(new_data)
            for i in [0, 2]:
                people.add(new_data[i])
        self.n_people = len(people)
        self.people = dict(zip(people, np.arange(self.n_people)))
        self.happiness = self.compute_happiness_matrix(happiness)

    def compute_happiness_matrix(self, happiness):
        n = self.n_people
        happiness_matrix = np.zeros((n, n), dtype=int)
        for h in happiness:
            i = self.people[h[0]]
            j = self.people[h[2]]
            happiness_matrix[i, j] = h[1]
        return happiness_matrix

    def find_max_happiness(self, include_self=False):
        n = self.n_people
        if include_self:
            n += 1
        s = np.arange(n)
        max_happiness = 0
        for order in permutations(s):
            happiness = 0
            for j in range(n):
                i = (j + 1) % n

                if (order[i] == self.n_people) or (order[j] == self.n_people):
                    continue

                happiness += self.happiness[order[j], order[i]]
                happiness += self.happiness[order[i], order[j]]

            if happiness > max_happiness:
                max_happiness = happiness

        return max_happiness


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    t = Table(data)

    print("Part 1")
    print(
        "The total change in happiness for the optimal "
        + f"seating arrangement is {t.find_max_happiness()}"
    )
    print()

    print("Part 2")
    print(
        "The total change in happiness for the optimal "
        + f"seating arrangement including you is {t.find_max_happiness(True)}"
    )


if __name__ == "__main__":
    main()
