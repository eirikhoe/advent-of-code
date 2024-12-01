from pathlib import Path
from time import sleep


def main():
    pos = [0, 1]
    recipes = [3, 7]
    index = 633601
    recipe_len = 10
    next_recipes = compute_next_recipes(pos, recipes, index, recipe_len)
    print(
        f"The scores of the next {recipe_len} recipes after {index} recipes are {next_recipes}."
    )

    pos = [0, 1]
    recipes = [3, 7]
    index = 633601
    recipe_number = compute_recipe_number(pos, recipes, index)
    print(f"{index} first appears after {recipe_number} recipes.")


def compute_next_recipes(pos, recipes, index, recipe_len):
    while len(recipes) < index + recipe_len:
        new_recipe = 0
        for p in pos:
            new_recipe += recipes[p]
        recipes += [int(d) for d in str(new_recipe)]

        for i, p in enumerate(pos):
            pos[i] = (pos[i] + 1 + recipes[p]) % len(recipes)

    return "".join([str(d) for d in recipes[index : index + recipe_len]])


def compute_recipe_number(pos, recipes, index):
    index = str(index)
    n = len(index)
    index = [int(d) for d in index]
    while True:
        new_recipe = 0
        for p in pos:
            new_recipe += recipes[p]
        recipes += [int(d) for d in str(new_recipe)]

        if len(recipes) >= n:
            match = True
            for i in range(1, n + 1):
                if recipes[-i] != index[-i]:
                    match = False
                    break
            if match:
                return len(recipes) - n

            if new_recipe >= 10:
                match = True
                for i in range(1, n + 1):
                    if recipes[-i - 1] != index[-i]:
                        match = False
                        break
                if match:
                    return len(recipes) - n - 1

        for i, p in enumerate(pos):
            pos[i] = (pos[i] + 1 + recipes[p]) % len(recipes)


if __name__ == "__main__":
    main()
