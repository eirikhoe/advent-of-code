from pathlib import Path
import re
from collections import deque

data_folder = Path(".").resolve()
reg = re.compile(r"(\d+) <-> (.+)")


def find_groups(comms):
    groups = []
    for i in range(len(comms)):
        in_groups = []
        for j in range(len(groups)):
            for k in range(len(comms[i])):
                if comms[i][k] in groups[j]:
                    in_groups.append(j)
                    break
        if not in_groups:
            groups.append(comms[i])
        else:
            for red_group in in_groups[-1:0:-1]:
                groups[in_groups[0]] += groups[red_group]
                del groups[red_group]
            groups[in_groups[0]] += comms[i]
            groups[in_groups[0]] = list(set(groups[in_groups[0]]))
    return groups


def main():
    data = data_folder.joinpath("input.txt").read_text()
    direct_comm = []
    for line in data.split("\n"):
        m = reg.match(line)
        l = [int(m.group(1))]
        l += l + [int(d) for d in m.group(2).split(", ")]
        l = list(set(l))
        direct_comm.append(l)

    print("Part 1")
    groups = find_groups(direct_comm)
    prog_id = 0
    len_prog_id_group = None
    for group in groups:
        if prog_id in group:
            len_prog_id_group = len(group)
            break

    print(
        f"There are {len_prog_id_group} programs in the group that contains program ID {prog_id}"
    )
    print()
    print("Part 2")
    print(f"There are {len(groups)} program groups in total")


if __name__ == "__main__":
    main()
