from pathlib import Path
from math import prod


def balance_groups(weights, n_groups, optimize=True):
    if sum(weights) % n_groups != 0:
        return None

    target = sum(weights) // n_groups
    weights = sorted(weights)
    weights = weights[::-1]
    optimal_number = len(weights) // n_groups
    initial_entanglement = prod(weights[:optimal_number]) + 1
    optimal_entanglement = initial_entanglement

    def recursion(chosen):
        nonlocal optimal_number
        nonlocal optimal_entanglement

        if (not optimize) and (optimal_entanglement < initial_entanglement):
            return

        n_chosen = len(chosen)
        chosen_weights = [weights[k] for k in chosen]
        total = sum(chosen_weights)

        if total > target:
            return

        if total == target:
            entanglement = prod(chosen_weights)
            if (n_chosen < optimal_number) or (entanglement < optimal_entanglement):
                rem_weights = [
                    weights[k] for k in range(len(weights)) if k not in chosen
                ]
                if (n_groups == 2) or (
                    balance_groups(rem_weights, n_groups - 1, False) is not None
                ):
                    optimal_number = n_chosen
                    optimal_entanglement = entanglement
            return

        if n_chosen >= optimal_number:
            return

        start = max(chosen)

        for i in range(start + 1, len(weights)):
            new_chosen = chosen.copy()
            new_chosen.append(i)
            recursion(new_chosen)

    for j in range(len(weights)):
        choice = [j]
        recursion(choice)

    return optimal_number, optimal_entanglement


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    weights = [int(w) for w in data.split("\n")]

    print("Part 1")
    n_groups = 3
    res = balance_groups(weights, n_groups)
    if res is not None:
        print(
            f"For {n_groups} groups, the optimal grouping has "
            + f"quantum entanglement {res[1]} for the first group"
        )
    print()

    print("Part 2")
    n_groups = 4
    res = balance_groups(weights, n_groups)
    if res is not None:
        print(
            f"For {n_groups} groups, the optimal grouping has "
            + f"quantum entanglement {res[1]} for the first group"
        )
    print()


if __name__ == "__main__":
    main()
