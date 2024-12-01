from pathlib import Path
import numpy as np
import re
from collections import deque

data_folder = Path(".").resolve()


class Bot:
    def __init__(self, pos, r):
        self.pos = pos
        self.r = r


class Bots:
    reg = re.compile(r"pos=<(-?\d+),(-?\d+),(-?\d+)>, r=(\d+)")

    def __init__(self, data):
        self.bots = []
        for line in data.split("\n"):
            m = Bots.reg.match(line).group(1, 2, 3, 4)
            m = [int(d) for d in m]
            self.bots.append(Bot(m[:3], m[3]))

    def dist(self, pos_a, pos_b):
        d = 0
        for i in range(3):
            d += abs(pos_a[i] - pos_b[i])
        return d

    def can_reach(self, ind):
        n = 0
        for i, bot in enumerate(self.bots):
            dist = self.dist(self.bots[ind].pos, bot.pos)
            if dist <= self.bots[ind].r:
                n += 1
        return n

    def strongest(self):
        r_max = -1
        max_ind = -1
        for i, bot in enumerate(self.bots):
            if bot.r > r_max:
                max_ind = i
                r_max = bot.r
        return max_ind

    def centroid(self):
        w = 0
        s = [0, 0, 0]
        for bot in self.bots:
            for j in range(3):
                s[j] += bot.pos[j] / bot.r
            w += 1 / bot.r
        for j in range(3):
            s[j] = int(s[j] / w)
        return s

    def in_reach(self, pos):
        n = 0
        for i, bot in enumerate(self.bots):
            dist = self.dist(pos, bot.pos)
            if dist <= bot.r:
                n += 1
        return n


def main():
    data = data_folder.joinpath("input.txt").read_text()
    print("Part 1:")
    b = Bots(data)
    strongest = b.strongest()
    print(f"The strongest nanobot has {b.can_reach(strongest)} nanobots in reach.")
    print()

    print("Part 2")
    guess = b.centroid()
    max_n = b.in_reach(guess)
    min_dist = b.dist(guess, (0, 0, 0))
    best_pos = guess
    for p in range(25, 1, -1):
        dim = 2**p
        step = 2 ** (p - 2)
        old_best_pos = (0, 0, 0)
        while old_best_pos != best_pos:
            old_best_pos = best_pos
            for i in range(-dim, dim + 1, step):
                for j in range(-dim, dim + 1, step):
                    for k in range(-dim, dim + 1, step):
                        pos = (
                            old_best_pos[0] + i,
                            old_best_pos[1] + j,
                            old_best_pos[2] + k,
                        )
                        n = b.in_reach(pos)
                        dist = b.dist(pos, (0, 0, 0))
                        if (n > max_n) or ((n == max_n) and (dist < min_dist)):
                            max_n = n
                            min_dist = dist
                            best_pos = pos

    print(
        f"The best point is in reach of {max_n} nanobots and is {min_dist} away from (0,0,0)."
    )


if __name__ == "__main__":
    main()
