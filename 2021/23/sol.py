from pathlib import Path

MOVE_COST = {1: 1, 2: 10, 3: 100, 4: 1000}


data_folder = Path(".").resolve()


def parse_data(data):
    lines = data.strip().split("\n")
    state = [0 for _ in range(7)]
    for j in [3, 5, 7, 9]:
        for i in range(2, len(lines) - 1):
            state.append(ord(lines[i][j]) - ord("A") + 1)
    state = tuple(state)
    return state


HALL_X = [0, 1, 3, 5, 7, 9, 10]


def room_size(state):
    return (len(state) - 7) // 4


def ind_to_pos(state, i):
    d = room_size(state)
    if i < 7:
        y = 0
        x = HALL_X[i]
    else:
        y = (i - 7) % d + 1
        x = 2 * ((i - 7) // d) + 2
    return y, x


def find_dist(state, i, j):
    yi, xi = ind_to_pos(state, i)
    yj, xj = ind_to_pos(state, j)
    if xi == xj:
        dist = abs(yi - yj)
    else:
        dist = yi + yj + abs(xi - xj)
    return dist


def get_door_ind(state, kind):
    d = room_size(state)
    door_ind = 7 + d * (kind - 1)
    return door_ind


def can_enter(state, kind):
    ok = True
    door_ind = get_door_ind(state, kind)
    depth = None
    if state[door_ind] != 0:
        return False, None
    for ind in range(door_ind + 1, door_ind + room_size(state)):
        if state[ind] not in {0, kind}:
            ok = False
            break
        elif state[ind] == kind:
            if depth is None:
                depth = ind - 1
    if ok and (depth is None):
        depth = door_ind + room_size(state) - 1
    return ok, depth


def get_hallway_ind(state, i):
    _, x = ind_to_pos(state, i)
    i = 2 + (x - 2) // 2
    return i


def get_available_hallway_ind(state, i):
    free = []
    if i >= 7:
        k = get_hallway_ind(state, i)
        for j in range(k - 1, -1, -1):
            if state[j] == 0:
                free.append(j)
            else:
                break
        for j in range(k, 7):
            if state[j] == 0:
                free.append(j)
            else:
                break

    return free


def find_legal_moves(state):
    moves = []
    for i in range(7):
        if state[i] > 0:
            enter, depth = can_enter(state, state[i])
            if enter:
                hallway_ind = get_hallway_ind(state, depth)
                if hallway_ind > i:
                    limits = [i + 1, hallway_ind]
                elif hallway_ind <= i:
                    limits = [hallway_ind, i]
                clear = True
                for k in range(limits[0], limits[1]):
                    if state[k] > 0:
                        clear = False
                if clear:
                    moves.append((i, depth))
    for r in range(4):
        door_ind = get_door_ind(state, r + 1)
        for i in range(door_ind, door_ind + room_size(state)):
            if state[i] > 0:
                enter, depth = can_enter(state, state[i])
                if (state[i] != r + 1) or (not enter):
                    for free in get_available_hallway_ind(state, i):
                        moves.append((i, free))
                if (state[i] != r + 1) and enter:
                    k = get_hallway_ind(state, i)
                    l = get_hallway_ind(state, depth)
                    clear = True
                    for p in range(min(k, l), max(k, l)):
                        if state[p] > 0:
                            clear = False
                            break
                    if clear:
                        moves.append((i, depth))
                break
    return moves


def print_state(state):
    int_to_chr = {0: ".", 1: "A", 2: "B", 3: "C", 4: "D"}
    s = ""
    s += "#" * 13 + "\n#"
    h = ["." for i in range(11)]
    for i, k in enumerate(HALL_X):
        h[k] = int_to_chr[state[i]]
    s += "".join(h) + "#\n"
    for i in range(room_size(state)):
        s += "##"
        for j in range(4):
            s += "#" + int_to_chr[state[7 + i + room_size(state) * j]]
        s += "###\n"
    s += "#" * 13 + "\n"
    print(s)


def solve(initial_state):
    final_state = tuple(
        [0 for _ in range(7)]
        + [i + 1 for i in range(4) for _ in range(room_size(initial_state))]
    )
    candidates = set()
    candidates.add(initial_state)
    min_cost = {initial_state: 0}
    while candidates:
        state = candidates.pop()
        for i, j in find_legal_moves(state):
            new_state = list(state)
            new_state[i], new_state[j] = new_state[j], new_state[i]
            new_state = tuple(new_state)

            move_cost = min_cost[state] + find_dist(state, i, j) * MOVE_COST[state[i]]

            if (new_state not in min_cost) or (move_cost < min_cost[new_state]):
                min_cost[new_state] = move_cost
                if new_state != final_state:
                    candidates.add(new_state)
    return min_cost[final_state]


def main():
    print("Part 1")
    data = data_folder.joinpath("input_1.txt").read_text()
    state = parse_data(data)
    min_cost = solve(state)
    print(f"The least energy required to organize the amphipods is {min_cost}")
    print()

    print("Part 2")
    data = data_folder.joinpath("input_2.txt").read_text()
    state = parse_data(data)
    min_cost = solve(state)
    print(
        f"The least energy required to organize the amphipods for the full diagram is {min_cost}"
    )

    print()


if __name__ == "__main__":
    main()
