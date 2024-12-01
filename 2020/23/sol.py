from pathlib import Path


def play(first_cups, n_moves, total_cups=None, n_neighbours=None):
    n_first_cups = len(first_cups)
    if n_neighbours is None:
        n_neighbours = n_first_cups - 1

    if total_cups is None:
        total_cups = n_first_cups

    right_value = list(range(1, total_cups + 1))
    right_value[-1] = first_cups[0] - 1
    for cup in first_cups:
        ind = first_cups.index(cup)
        if ind == n_first_cups - 1:
            if total_cups > n_first_cups:
                right_value[cup - 1] = n_first_cups
            else:
                right_value[cup - 1] = first_cups[0] - 1

        else:
            right_value[cup - 1] = first_cups[ind + 1] - 1

    current = first_cups[0] - 1
    pick_up = [0, 0, 0]
    for i in range(n_moves):
        ind = current
        for j in range(3):
            pick_up[j] = right_value[ind]
            ind = pick_up[j]
        target = (current - 1) % total_cups
        while target in pick_up:
            target = (target - 1) % total_cups
        right_value[current] = right_value[pick_up[-1]]
        temp = right_value[target]
        right_value[target] = pick_up[0]
        right_value[pick_up[-1]] = temp
        current = right_value[current]

    val = 0
    res = []
    for i in range(n_neighbours):
        val = right_value[val]
        res.append(val + 1)

    return res


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    cups = [int(d) for d in data]

    n_moves = 100
    final = play(cups, n_moves)
    cup_str = "".join([str(d) for d in final])
    print("Part 1")
    print(f"After {n_moves} moves the labels on the cups ")
    print(f"after cup 1 is {cup_str}")
    print()

    n_moves = 10_000_000
    n_cups = 1_000_000
    final = play(cups, n_moves, total_cups=n_cups, n_neighbours=2)
    print("Part 2")
    print(f"After {n_moves} moves with {n_cups} cups the cups with ")
    print(f"labels {final[0]} and {final[1]} are immediately clockwise ")
    print(f"of cup 1. Multiplying their labels give {final[0]*final[1]}")
    print()


if __name__ == "__main__":
    main()
