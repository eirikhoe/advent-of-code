from pathlib import Path
import numpy as np
import copy
import re

data_folder = Path(__file__).parent.resolve()


class Eris:
    def __init__(self, file):
        state = [[ord(d) for d in list(x)] for x in file.read_text().split("\n")]
        self.state = (np.array(state, dtype=int) == ord("#")).astype(int)
        self.diversities = [self.compute_biodiversity]

    def find_nearby_bugs(self):
        nearby_bugs = np.zeros(self.state.shape, int)
        nearby_bugs[:, 1:] += self.state[:, :-1]
        nearby_bugs[:, :-1] += self.state[:, 1:]
        nearby_bugs[1:, :] += self.state[:-1, :]
        nearby_bugs[:-1, :] += self.state[1:, :]
        return nearby_bugs

    def advance_state(self):
        nearby_bugs = self.find_nearby_bugs()
        old_state = np.copy(self.state)
        self.state[(old_state == 1) & (nearby_bugs != 1)] = 0
        self.state[(old_state == 0) & ((nearby_bugs == 1) | (nearby_bugs == 2))] = 1

    def print_state(self):
        print(
            "\n".join(
                [
                    "".join([str(d) for d in row]).replace("1", "#").replace("0", ".")
                    for row in self.state
                ]
            )
        )

    def compute_biodiversity(self):
        flattened = self.state.flatten()
        return np.sum(2 ** np.arange(flattened.size)[flattened.astype(bool)])

    def advance_state_til_repeat(self):
        self.advance_state()
        biodiversity = self.compute_biodiversity()

        # biodiversity and state is one to one
        while biodiversity not in self.diversities:
            self.diversities.append(biodiversity)
            self.advance_state()
            biodiversity = self.compute_biodiversity()
        print(f"The biodiversity is {biodiversity} for the first state that repeats")


def main():
    file = data_folder / "day_24_input.txt"
    eris = Eris(file)
    eris.advance_state_til_repeat()


if __name__ == "__main__":
    main()

