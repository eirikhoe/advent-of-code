from pathlib import Path

data_folder = Path(__file__).parent.resolve()


def find_combinations(data, vol, use_minimum_containers=False):
    containers = [int(d) for d in data.split("\n")]
    n_containers = []
    _find_comb(vol, containers, 0, n_containers)
    min_containers = min(n_containers)
    combinations = 0
    if use_minimum_containers:
        for option in n_containers:
            if option == min_containers:
                combinations += 1
        return combinations
    return len(n_containers)


def _find_comb(vol, containers, taken, n_containers):
    if vol < 0:
        return None
    elif vol == 0:
        n_containers.append(taken)
        return None
    elif sum(containers) < vol:
        return None
    else:
        _find_comb(vol - containers[0], containers[1:], taken + 1, n_containers)
        _find_comb(vol, containers[1:], taken, n_containers)
        return None


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    volume = 150
    print("Part 1")
    print(
        f"There are {find_combinations(data,volume)} combinations that "
        + f"can exactly fit {volume} litres of eggnog"
    )
    print()
    print("Part 2")
    print(
        f"There are {find_combinations(data,volume,True)} combinations that "
        + f"can exactly fit {volume} litres of eggnog using a minimum number "
        + "of containers"
    )


if __name__ == "__main__":
    main()
