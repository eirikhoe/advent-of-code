from pathlib import Path
import re
from copy import deepcopy
from collections import deque
import itertools

data_folder = Path(".").resolve()
valve_reg = re.compile(
    r"Valve ([A-Z]+) has flow rate=(\d+); tunnels? leads? to valves? ((?:[A-Z]+(?:, )?)+)"
)


class Valves:
    def __init__(self, data):
        flow_rates = dict()
        neighbours = dict()
        id = dict()
        for i, line in enumerate(data.split("\n")):
            groups = valve_reg.match(line).groups()
            name = groups[0]
            flow_rates[name] = int(groups[1])
            neighbours[name] = tuple(groups[2].split(", "))
            id[name] = i
        self.flow_rates = flow_rates
        self.neighbours = neighbours
        self.id = id

    def _make_index(self, state):
        return tuple(sorted(state[0]))

    def _get_candidates(self, state, time_limit):
        candidates = []
        n_people = len(state[0])
        options = [range(1 + len(self.neighbours[name])) for name in state[0]]
        minutes_passed = state[1] + 1
        for option in itertools.product(*options):
            released = state[2]
            pos = list(state[0])
            closed = list(state[3])
            valid = True
            came_from = list(state[4])
            for j in range(n_people):
                name = state[0][j]
                if option[j] == 0:
                    if closed[self.id[name]] and (self.flow_rates[name] > 0):
                        closed[self.id[name]] = False
                        released += (time_limit - minutes_passed) * self.flow_rates[name]
                        came_from[j] = None
                    else:
                        valid = False
                        break
                else:
                    dest = self.neighbours[name][option[j] - 1]
                    if came_from[j] != dest:
                        pos[j] = self.neighbours[name][option[j] - 1]
                        came_from[j] = name
                    else:
                        valid = False
                        break
            if valid:
                candidates.append(
                    (
                        tuple(pos),
                        minutes_passed,
                        released,
                        tuple(closed),
                        tuple(came_from),
                    )
                )
        return candidates

    def find_max_pressure_release(self, start_valve, time_limit, n_people):
        states = deque(
            [
                (
                    tuple(start_valve for i in range(n_people)),
                    0,
                    0,
                    tuple(True for _ in range(len(self.flow_rates))),
                    tuple(None for _ in range(n_people)),
                )
            ]
        )
        positive_flow_rate = [name for name in self.flow_rates if self.flow_rates[name] > 0]
        max_pressure_release = 0
        best = {}
        curr_min = 0
        while len(states) > 0:
            state = states.pop()
            if state[1] > curr_min:
                best = {}
                curr_min = state[1]

            if state[2] > max_pressure_release:
                max_pressure_release = state[2]
            if state[1] == time_limit:
                continue

            # Prune if better state has been observed
            index = self._make_index(state)
            opened = {i for i, s in enumerate(state[3]) if not s}
            if index not in best:
                best[index] = [(state[2], opened)]
            else:
                match = False
                i = 0
                to_delete = set()
                while i < len(best[index]):
                    if (state[2] <= best[index][i][0]) and opened.issubset(best[index][i][1]):
                        match = True
                        break
                    elif (state[2] >= best[index][i][0]) and best[index][i][1].issubset(opened):
                        to_delete.add(i)
                    i += 1
                if len(to_delete) > 0:
                    best[index] = [i for j, i in enumerate(best[index]) if j not in to_delete]
                if match:
                    continue
                else:
                    best[index].append((state[2], opened))

            # Prune if current state has an upper limit below current best
            missing = []
            for valve in positive_flow_rate:
                if state[3][self.id[valve]]:
                    missing.append(self.flow_rates[valve])
            missing.sort()
            upper_limit = state[2]
            time = state[1] + 1
            while time < time_limit:
                for _ in range(n_people):
                    if len(missing) == 0:
                        break
                    flow = missing.pop()
                    upper_limit += flow * (time_limit - time)
                time += 2
            if upper_limit <= max_pressure_release:
                continue

            for cand in self._get_candidates(state, time_limit):
                states.appendleft(cand)
        return max_pressure_release


def main():
    data = data_folder.joinpath("input.txt").read_text()
    valves = Valves(data)

    print("Part 1")
    time_limit = 30
    n_people = 1
    max_pressure_release = valves.find_max_pressure_release("AA", time_limit, n_people)
    print(f"The max pressure you can release in {time_limit} minutes with {n_people} people is {max_pressure_release}.")
    print()

    print("Part 2")
    time_limit = 26
    n_people = 2
    max_pressure_release = valves.find_max_pressure_release("AA", time_limit, n_people)
    print(f"The max pressure you can release in {time_limit} minutes with {n_people} people is {max_pressure_release}.")
    print()


if __name__ == "__main__":
    main()
