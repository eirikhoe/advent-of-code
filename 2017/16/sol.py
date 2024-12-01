from pathlib import Path
import numpy as np
from collections import deque
import re

data_folder = Path(".").resolve()


class Dance:
    def __init__(self, data, n):
        self.int_order = np.arange(n)
        self.moves = data.split(",")
        self.n_dancers = n
        self.int_moves = None
        self.rename = None

    def dance(self):
        if self.int_moves is None:
            init_order = list(range(self.n_dancers))
            self.int_moves = deque(init_order)
            self.str_moves = np.copy(init_order)
            for move in self.moves:
                if move[0] == "s":
                    self.spin(move[1:])
                elif move[0] == "x":
                    self.exchange(move[1:])
                elif move[0] == "p":
                    self.partner(move[1:])
            self.rename = dict(zip(init_order, self.str_moves))
            self.int_moves = np.array(list(self.int_moves))

        self.int_order = self.int_order[self.int_moves]
        for i, prog in enumerate(self.int_order):
            self.int_order[i] = self.rename[prog]

    def spin(self, instr):
        rot = int(instr)
        self.int_moves.rotate(rot)

    def exchange(self, instr):
        pos = [int(d) for d in instr.split("/")]
        temp = self.int_moves[pos[0]]
        self.int_moves[pos[0]] = self.int_moves[pos[1]]
        self.int_moves[pos[1]] = temp

    def partner(self, instr):
        progs = [ord(d) - 97 for d in instr.split("/")]
        pos = [-1, -1]
        ind = 0
        for j, prog in enumerate(self.str_moves):
            if prog in progs:
                pos[ind] = j
                ind += 1
        temp = self.str_moves[pos[0]]
        self.str_moves[pos[0]] = self.str_moves[pos[1]]
        self.str_moves[pos[1]] = temp

    def order(self):
        s = ""
        for prog_int in self.int_order:
            s += chr(prog_int + 97)
        return s

    def repeated_dance(self, n):
        k = 0
        powers = []
        bin_n = [int(d) for d in list(bin(n)[2:])[::-1]]
        for j, bit in enumerate(bin_n):
            if bit:
                powers.append(j)
        if self.int_moves is None:
            self.dance()

        curr_int_dance = self.int_moves
        curr_rename = self.rename
        int_dance_powers = []
        rename_powers = []

        power_ind = 0
        ind = 0

        while power_ind < len(powers):
            while ind < powers[power_ind]:
                curr_int_dance = curr_int_dance[curr_int_dance]
                old_rename = curr_rename.copy()
                for key in curr_rename:
                    curr_rename[key] = old_rename[old_rename[key]]
                ind += 1
            int_dance_powers.append(curr_int_dance)
            rename_powers.append(curr_rename.copy())
            power_ind += 1

        final_order = np.arange(self.n_dancers)
        for moves in int_dance_powers:
            final_order = final_order[moves]

        for rename in rename_powers:
            for i, prog in enumerate(final_order):
                final_order[i] = rename[prog]

        self.int_order = final_order


def main():
    data = data_folder.joinpath("input.txt").read_text()
    d = Dance(data, 16)

    print("Part 1")
    d.dance()
    print(f"The programs are standing in the order {d.order()} after the dance")
    print()

    print("Part 2")
    n_dances = int(1e9)
    d.repeated_dance(n_dances)
    print(f"The programs are standing in the order {d.order()} after {n_dances} dances")


if __name__ == "__main__":
    main()
