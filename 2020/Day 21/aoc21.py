from pathlib import Path
import re
from collections import defaultdict
import numpy as np

ingredient_re = re.compile(r"([a-z ]+)\(contains ([a-z ,]+)\)")


def parse_data(data):
    ingredients = []
    allergens = []
    for line in data.split("\n"):
        m = ingredient_re.match(line)
        if m is None:
            raise RuntimeError("Incorrect data")
        g = m.groups()
        ingredient_list = g[0].strip().split()
        allergen_list = g[1].strip().split(", ")
        allergens.append(allergen_list)
        ingredients.append(ingredient_list)
    return ingredients, allergens


def solve_allergies(ingredients, allergens):

    danger_cand = dict()
    inert = set()
    for j, allergens_per_food in enumerate(allergens):
        for allergen in allergens_per_food:
            if allergen in danger_cand:
                danger_cand[allergen] &= set(ingredients[j])
            else:
                danger_cand[allergen] = set(ingredients[j])
        inert |= set(ingredients[j])
    for allergen in danger_cand:
        inert -= danger_cand[allergen]

    n_inert = 0
    for ingredients_per_food in ingredients:
        for ingredient in ingredients_per_food:
            if ingredient in inert:
                n_inert += 1

    max_len = 2
    while max_len > 1:
        max_len = 1
        for allergen in danger_cand:
            if len(danger_cand[allergen]) == 1:
                for other in danger_cand:
                    if other != allergen:
                        danger_cand[other] -= danger_cand[allergen]
        for allergen in danger_cand:
            if len(danger_cand[allergen]) > max_len:
                max_len = len(danger_cand[allergen])

    allergens = []
    danger_ingredients = []
    for allergen in danger_cand:
        allergens.append(allergen)
        danger_ingredients.append(danger_cand[allergen].pop())

    order = np.argsort(allergens)
    cdil = np.array(danger_ingredients)[order]
    cdil_str = ",".join(cdil)

    return n_inert, cdil_str


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    ingredients, allergens = parse_data(data)
    n_inert, cdil = solve_allergies(ingredients, allergens)

    print("Part 1")
    print(f"The inert ingredients appear {n_inert} times in the food list")
    print()

    print("Part 2")
    print("The canonical dangerous ingredient list is:")
    print(cdil)


if __name__ == "__main__":
    main()
