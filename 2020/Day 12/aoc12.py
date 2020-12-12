from pathlib import Path

directions = {"E": [0, 1], "W": [0, -1], "N": [-1, 0], "S": [1, 0]}
headings = ["E", "N", "W", "S"]
turn_sgn = {"L": 1, "R": -1}

def turn_right(v,deg):
    if deg not in [0,90,180,270]:
        raise RuntimeError("Invalid degrees")

    if deg == 90:
        return [-v[1],v[0]]
    elif deg == 180:
        return [-v[0],-v[1]]
    elif deg == 270:
        return [v[1],-v[0]]
    return v


def find_ferry_distance(instrs):
    instrs = [[instr[0], int(instr[1:])] for instr in instrs]
    heading = [0, 1]
    pos = [0, 0]
    for instr in instrs:
        if instr[0] in ["R", "L"]:
            deg = (instr[1]*turn_sgn[instr[0]]) % 360
            heading = turn_right(heading,deg)
        else:
            if instr[0] in directions:
                curr_dir = directions[instr[0]]
            elif instr[0] == "F":
                curr_dir = heading
            else:
                raise RuntimeError("Invalid action")
            pos[0] += curr_dir[0] * instr[1]
            pos[1] += curr_dir[1] * instr[1]
    man_dist = abs(pos[0]) + abs(pos[1])
    return man_dist


def find_ferry_distance_with_waypoint(instrs):
    instrs = [[instr[0], int(instr[1:])] for instr in instrs]
    waypoint = [-1, 10]
    pos = [0, 0]
    for instr in instrs:
        if instr[0] in ["R", "L"]:
            deg = (instr[1]*turn_sgn[instr[0]]) % 360
            waypoint = turn_right(waypoint,deg)
        elif instr[0] in directions:
            curr_dir = directions[instr[0]]
            waypoint[0] += curr_dir[0] * instr[1]
            waypoint[1] += curr_dir[1] * instr[1]
        elif instr[0] == "F":
            pos[0] += waypoint[0] * instr[1]
            pos[1] += waypoint[1] * instr[1]
        else:
            raise RuntimeError("Invalid action")
    man_dist = abs(pos[0]) + abs(pos[1])
    return man_dist


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    instrs = data.split("\n")
    print("Part 1")
    man_dist = find_ferry_distance(instrs)
    print("The Manhattan distance between the ship's starting and final ")
    print(f"position is {man_dist}")
    print()

    print("Part 2")
    man_dist = find_ferry_distance_with_waypoint(instrs)
    print("The Manhattan distance between the ship's starting and final ")
    print(f"position with the waypoint is {man_dist}")


if __name__ == "__main__":
    main()
