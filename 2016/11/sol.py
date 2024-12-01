from pathlib import Path
from collections import deque
import re
import numpy as np

data_folder = Path(".").resolve()

reg_floor = re.compile(r"an? (\w+)(-compatible microchip| generator)")


class Factory:
    def __init__(self, data):
        locations = dict()
        item_index = {"-compatible microchip": 0, " generator": 1}
        for i, line in enumerate(data.split("\n")):
            for item in reg_floor.findall(line):
                if item[0] not in locations:
                    locations[item[0]] = [None, None]
                locations[item[0]][item_index[item[1]]] = i
        self.state = [0] + [tuple(locations[element]) for element in locations]
        self.state = tuple(self.state)
        self.seen_states = {self.state: 0}

    def find_optimal_route(self):
        candidates = deque([[self.state, 0]])
        end_state = [3] + [(3, 3) for locs in self.state[1:]]
        end_state = tuple(end_state)
        while self.state != end_state:
            self.state, n_moves = candidates.pop()
            for state_candidate in self._possible_moves():
                if state_candidate not in self.seen_states:
                    self.seen_states[state_candidate] = n_moves + 1
                    candidates.appendleft([state_candidate, n_moves + 1])

        return self.seen_states[end_state]

    def _possible_moves(self):
        same_floor_indexes = []
        elevator_floor = self.state[0]
        valid_new_states = []
        for i in range(1, len(self.state)):
            for j in range(2):
                if self.state[i][j] == elevator_floor:
                    same_floor_indexes.append((i, j))
        if elevator_floor == 0:
            new_floors = [1]
        elif elevator_floor == 3:
            new_floors = [2]
        else:
            new_floors = [elevator_floor - 1, elevator_floor + 1]

        for floor in new_floors:
            for k, item_index in enumerate(same_floor_indexes):
                i, j = item_index
                new_state = list(self.state)
                new_state[0] = floor
                new_state[i] = list(new_state[i])
                new_state[i][j] = floor
                new_state[i] = tuple(new_state[i])
                if not self._fried(new_state):
                    valid_new_states.append(tuple(new_state))
                for l in range(k + 1, len(same_floor_indexes)):
                    q, p = same_floor_indexes[l]
                    newer_state = new_state.copy()
                    newer_state[q] = list(newer_state[q])
                    newer_state[q][p] = floor
                    newer_state[q] = tuple(newer_state[q])
                    if not self._fried(newer_state):
                        valid_new_states.append(tuple(newer_state))
        return valid_new_states

    def _fried(self, state):
        generator_locs = [item[1] for item in state[1:]]
        fried = False
        for i in range(1, len(state)):
            if (state[i][1] != state[i][0]) and (state[i][0] in generator_locs):
                fried = True
                break
        return fried


def main():
    data = data_folder.joinpath("input_1.txt").read_text()
    f = Factory(data)

    print("Part 1")
    print(
        f"It takes a minimum of {f.find_optimal_route()} steps to get all the parts up to the assembly"
    )
    print()

    data = data_folder.joinpath("input_2.txt").read_text()
    f = Factory(data)

    print("Part 2")
    print(
        f"It takes a minimum of {f.find_optimal_route()} steps to get all the parts up to the assembly"
    )
    print()


if __name__ == "__main__":
    main()
