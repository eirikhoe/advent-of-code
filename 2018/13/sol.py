from pathlib import Path
import numpy as np
import re
from bisect import bisect_left
from collections import deque
from copy import deepcopy


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text().split("\n")
    data = [list(line) for line in data]
    track = Track(data)
    colision_point = track.move_until_colision()
    print(f"First crash at point {colision_point}.")
    track.print_track()

    track = Track(data)
    last_point = track.move_until_last()
    print(f"Last car at point {last_point}.")
    track.print_track()


class Cart:
    def __init__(self, pos, orientation):
        self.pos = pos
        self.orientation = orientation
        self.intersect_choice = deque("LSR")


class Track:
    right = {(1, 0): "\\", (-1, 0): "\\", (0, 1): "/", (0, -1): "/"}
    left = {(1, 0): "/", (-1, 0): "/", (0, 1): "\\", (0, -1): "\\"}
    symbol = {(1, 0): ">", (-1, 0): "<", (0, -1): "^", (0, 1): "v"}
    direction = {">": (1, 0), "<": (-1, 0), "^": (0, -1), "v": (0, 1)}

    @classmethod
    def rot(self, v, type):
        rotated = {"R": (-v[1], v[0]), "L": (v[1], -v[0]), "S": v}
        return rotated[type]

    def __init__(self, data):
        data = deepcopy(data)
        self.carts = []
        for y, row in enumerate(data):
            for x, char in enumerate(row):
                if char in ["<", ">"]:
                    self.carts.append(Cart((x, y), Track.direction[char]))
                    data[y][x] = "-"
                elif char in ["^", "v"]:
                    self.carts.append(Cart((x, y), Track.direction[char]))
                    data[y][x] = "|"
        self.track = data

    def move_cart(self, cart):
        x, y = cart.pos
        if self.track[y][x] in Track.right[cart.orientation]:
            cart.orientation = Track.rot(cart.orientation, "R")
        elif self.track[y][x] in Track.left[cart.orientation]:
            cart.orientation = Track.rot(cart.orientation, "L")
        elif self.track[y][x] == "+":
            cart.orientation = Track.rot(cart.orientation, cart.intersect_choice[0])
            cart.intersect_choice.rotate(-1)
        vx, vy = cart.orientation
        cart.pos = (x + vx, y + vy)

    def move_until_colision(self):
        while True:
            positions = []
            for cart in self.carts:
                x, y = cart.pos
                positions.append(y * (len(self.track[0]) - 1) + x)

            order = np.argsort(positions)
            t = 0
            for i in order:
                self.move_cart(self.carts[i])
                for j, cart in enumerate(self.carts):
                    if (i != j) and (cart.pos == self.carts[i].pos):
                        return self.carts[i].pos
            t += 1

    def move_until_last(self):
        t = 0
        while True:
            positions = []
            for cart in self.carts:
                x, y = cart.pos
                positions.append(y * (len(self.track[0]) - 1) + x)

            order = list(np.argsort(positions))
            i = 0
            while i < len(order):
                self.move_cart(self.carts[order[i]])
                j = 0
                i_delta = 1
                while j < len(order):
                    if (order[i] != order[j]) and (
                        self.carts[order[j]].pos == self.carts[order[i]].pos
                    ):
                        del self.carts[order[i]]
                        if order[j] > order[i]:
                            del self.carts[order[j] - 1]
                        else:
                            del self.carts[order[j]]

                        i_delta = 0
                        if j < i:
                            i_delta = -1
                        for k in range(len(order)):
                            red = 0
                            if order[k] > order[i]:
                                red -= 1
                            if order[k] > order[j]:
                                red -= 1
                            order[k] += red

                        del order[i]
                        if j > i:
                            del order[j - 1]
                        else:
                            del order[j]
                        break
                    else:
                        j += 1
                i += i_delta

            if len(self.carts) == 1:
                return self.carts[0].pos
            t += 1

    def print_track(self):
        track = deepcopy(self.track)
        for cart in self.carts:
            x, y = cart.pos
            if track[y][x] in list(Track.direction.keys()):
                track[y][x] = "X"
            else:
                track[y][x] = Track.symbol[cart.orientation]

        s = ""
        col_size = len(track[0])
        col_digits = len(str(col_size - 1))
        form_str = "{:" + str(col_digits) + "d}"
        for j in range(col_digits):
            s += " "
            for loc in range(col_size):
                loc_str = form_str.format(loc)
                s += loc_str[j]
            s += "\n"

        row_size = len(track)
        row_digits = len(str(row_size - 1))
        form_str = "{:" + str(row_digits) + "d}"
        for y in range(row_size):
            s += form_str.format(y)
            s += "".join(track[y])
            s += "\n"
        print(s)


if __name__ == "__main__":
    main()
