from pathlib import Path
import numpy as np
import re

data_folder = Path(__file__).parent.resolve()

reg_ingredient = re.compile(r"(\w+): (.+)")


class Cookie:
    def __init__(self, data, calorie_lim):
        self.ingredients = []
        self.property_names = None
        self.properties = []
        for line in data.split("\n"):
            m = reg_ingredient.match(line)
            assert m is not None
            self.ingredients.append(m.group(1))
            info = m.group(2).split(", ")
            info = [d.split(" ") for d in info]
            if self.property_names is None:
                self.property_names = [d[0] for d in info]
            self.properties.append([int(d[1]) for d in info])
        self.properties = np.array(self.properties, dtype=int)
        self.calories = self.properties[:, -1]
        self.properties = self.properties[:, :-1]
        self.calorie_lim = calorie_lim
        self.current = None
        self.max_score = 0
        self.max_score_calorie = 0

    def find_optimal_recipe(self, depth=0):
        n = len(self.ingredients)
        if depth == 0:
            self.current = np.zeros(n, dtype=int)

        for i in range(101 - np.sum(self.current)):
            self.current[depth] = i
            if depth < n - 1:
                self.find_optimal_recipe(depth + 1)
            else:
                property_scores = np.matmul(self.current, self.properties)
                property_scores[property_scores < 0] = 0
                score = np.prod(property_scores)
                if score > self.max_score:
                    self.max_score = score
                calories = np.dot(self.current, self.calories)
                if (calories == self.calorie_lim) and (score > self.max_score_calorie):
                    self.max_score_calorie = score

        self.current[depth] = 0


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    calorie_lim = 500
    c = Cookie(data, calorie_lim)
    c.find_optimal_recipe()
    print("Part 1")
    print(f"The best recipe has the score {c.max_score}")
    print()

    print("Part 2")
    print(
        f"The best recipe with exactly {calorie_lim} calories "
        + f"has the score {c.max_score_calorie}"
    )


if __name__ == "__main__":
    main()
