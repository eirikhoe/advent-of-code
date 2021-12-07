from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    data = [int(d) for d in data.split(",")]
    return data


def sim_fish(intitial_pop, n_days):
    future_births = [0] * 9
    for fish in intitial_pop:
        future_births[fish] += 1
    for _ in range(n_days):
        n_births = future_births[0]
        future_births[:-1] = future_births[1:]
        future_births[6] += n_births
        future_births[8] = n_births
    return sum(future_births)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    initial_pop = parse_data(data)

    print("Part 1")
    n_days = 80
    print(f"After {n_days} days there are {sim_fish(initial_pop,n_days)} fish")
    print()

    print("Part 2")
    n_days = 256
    print(f"After {n_days} days there are {sim_fish(initial_pop,n_days)} fish")
    print()


if __name__ == "__main__":
    main()
