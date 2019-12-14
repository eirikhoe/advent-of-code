from pathlib import Path
import numpy as np
import re
from math import ceil
import copy
from collections import OrderedDict

data_folder = Path(__file__).parent.resolve()
file = data_folder / "day_14_input.txt"
find_ingredients = re.compile(r"(\d+ \w+)+")


class Ingredient:
    def __init__(self, name, quantity):
        self.name = name
        self.quantity = int(quantity)

class Reaction:
    def __init__(self, recipe):
        ingredients = find_ingredients.findall(recipe)
        for i in np.arange(len(ingredients)):
            ingredients[i] = ingredients[i].split(" ")
            ingredients[i] = Ingredient(ingredients[i][1], ingredients[i][0])
        self.reactants = dict(
            zip(
                [ingredient.name for ingredient in ingredients[:-1]],
                [ingredient.quantity for ingredient in ingredients[:-1]],
            )
        )
        self.product = ingredients[-1]
        self.n_reactants = len(self.reactants)

class Reactions:
    def __init__(self, reactions):
        self.reactions = dict(
            zip([reaction.product.name for reaction in reactions], reactions)
        )

    def total_reactants(self, chemical):
        total = set()
        if chemical == "ORE":
            return total
        for name in self.reactions[chemical].reactants.keys():
            total = total.union(self.total_reactants(name)).union({name})
        return total

    def get_ore_cost(self, ingredient):
        if ingredient.name == "ORE":
            return ingredient.quantity
        reaction = self.reactions[ingredient.name]
        multiple = ceil(ingredient.quantity / reaction.product.quantity)
        ingredients = copy.deepcopy(reaction.reactants)
        for name in ingredients.keys():
            ingredients[name] *= multiple
        while (len(ingredients.keys()) > 1) or (list(ingredients.keys())[0] != "ORE"):
            for curr_ingredient_name in ingredients.keys():
                if curr_ingredient_name != "ORE":
                    total_reactants_other = set()
                    for name in ingredients.keys():
                        if name != curr_ingredient_name:
                            total_reactants_other = total_reactants_other.union(
                                self.total_reactants(name)
                            )
                    if curr_ingredient_name not in total_reactants_other:
                        ingredients = self._replace_ingredient_with_reactants(
                            curr_ingredient_name, ingredients
                        )
                        break
        return ingredients["ORE"]

    def _replace_ingredient_with_reactants(self, ingredient_name, ingredients):
        multiple = ceil(
            ingredients[ingredient_name]
            / self.reactions[ingredient_name].product.quantity
        )
        for reactant_name in self.reactions[ingredient_name].reactants.keys():
            added_reactant = (
                multiple * self.reactions[ingredient_name].reactants[reactant_name]
            )

            if reactant_name in ingredients:
                ingredients[reactant_name] += added_reactant
            else:
                ingredients[reactant_name] = added_reactant

        del ingredients[ingredient_name]
        return ingredients

    def get_max_fuel(self, ore_reserve):
        fuel = Ingredient("FUEL", 1)
        unit_cost = self.get_ore_cost(fuel)
        l = ore_reserve // unit_cost
        fuel.quantity = l
        if self.get_ore_cost(fuel) == ore_reserve:
            return fuel.quantity
        r = l * 2
        fuel.quantity = r
        while self.get_ore_cost(fuel) <= ore_reserve:
            r *= 2
            fuel.quantity = r

        while r - l > 1:
            mid = (r + l) // 2
            fuel.quantity = mid
            cost = self.get_ore_cost(fuel)
            if cost == ore_reserve:
                return mid
            elif cost < ore_reserve:
                l = mid
            else:
                r = mid
        return l


def main():
    r = Reactions([Reaction(reaction) for reaction in file.read_text().split("\n")])
    ingredient = Ingredient("FUEL", 1)
    print("Part 1")
    print(
        f"The minimum cost of producing one unit of FUEL is {r.get_ore_cost(ingredient)} ORE"
    )

    print("Part 2")
    ore_reserve = 1000000000000
    print(
        f"The maximum amount of FUEL that can be produced for\n{ore_reserve} ORE is {r.get_max_fuel(ore_reserve)} FUEL"
    )


if __name__ == "__main__":
    main()
