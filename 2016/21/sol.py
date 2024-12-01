from pathlib import Path
import numpy as np
from collections import deque
import re

data_folder = Path(".").resolve()


class Password:
    def __init__(self, moves, initial_string):
        self.password = list(initial_string)
        self.moves = self.interpret(moves.split("\n"))

    def interpret(self, moves):
        operations = [
            r"swap position (\d+) with position (\d+)",
            r"swap letter ([a-zA-Z]) with letter ([a-zA-Z])",
            r"rotate (left|right) (\d+)",
            r"rotate based on position of letter ([a-zA-Z])",
            r"reverse positions (\d+) through (\d+)",
            r"move position (\d+) to position (\d+)",
        ]
        operations = [re.compile(move) for move in operations]
        interpreted_moves = []
        for move in moves:
            for j, operation in enumerate(operations):
                m = operation.match(move)
                if m is not None:
                    interpreted_moves.append([j, m.groups()])
                    break
        return interpreted_moves

    def rotate_abs(self, instr, reversed):
        rot = int(instr[1])
        if instr[0] == "left":
            rot = -rot
        if reversed:
            rot = -rot

        rot = rot % len(self.password)

        self.password = self.password[-rot:] + self.password[:-rot]

    def swap_pos(self, instr, reversed):
        pos = [int(d) for d in instr]
        temp = self.password[pos[0]]
        self.password[pos[0]] = self.password[pos[1]]
        self.password[pos[1]] = temp

    def swap_letter(self, instr, reversed):
        pos = [-1, -1]
        ind = 0
        for j, char in enumerate(self.password):
            if char in instr:
                pos[ind] = j
                ind += 1
        temp = self.password[pos[0]]
        self.password[pos[0]] = self.password[pos[1]]
        self.password[pos[1]] = temp

    def rotate_pos(self, instr, reversed):
        ind = 0
        for j, char in enumerate(self.password):
            if char == instr[0]:
                ind = j
                break
        if reversed:
            if len(self.password) == 8:
                reverse_lookup = [1, 3, 5, 7, 2, 4, 6, 0]
                for j, pos in enumerate(reverse_lookup):
                    if ind == pos:
                        ind = j
                        break
        n_rots = 1 + ind + int(ind >= 4)
        self.rotate_abs(("right", n_rots), reversed)

    def reverse(self, instr, reversed):
        pos = [int(d) for d in instr]
        part = self.password[pos[0] : (pos[1] + 1)].copy()
        reversed_part = part[::-1]
        self.password[pos[0] : (pos[1] + 1)] = reversed_part

    def move(self, instr, reversed):
        pos = [int(d) for d in instr]

        if reversed:
            pos = pos[::-1]

        char = self.password[pos[0]]
        if pos[0] < pos[1]:
            self.password[pos[0] : pos[1]] = self.password[(pos[0] + 1) : (pos[1] + 1)]
        elif pos[1] < pos[0]:
            self.password[(pos[1] + 1) : (pos[0] + 1)] = self.password[pos[1] : pos[0]]

        self.password[pos[1]] = char

    operations = [swap_pos, swap_letter, rotate_abs, rotate_pos, reverse, move]

    def operate(self, op_ind, instr, reversed=False):
        op = Password.operations[op_ind]
        op(self, instr, reversed)

    def scramble(self):
        for move in self.moves:
            self.operate(move[0], move[1])

    def descramble(self):
        for move in self.moves[::-1]:
            self.operate(move[0], move[1], True)

    def get_password(self):
        return "".join(self.password)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    p = Password(data, "abcdefgh")
    p.scramble()
    print("Part 1")
    print(f"The scrambled password is {p.get_password()}")
    print()

    p = Password(data, "fbgdceah")
    p.descramble()
    print("Part 2")
    print(f"The unscrambled password is {p.get_password()}")


if __name__ == "__main__":
    main()
