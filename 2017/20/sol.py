from pathlib import Path
import numpy as np
import re
from collections import defaultdict
import re
from collections import deque

reg = re.compile(
    r"p=< *(-?\d+), *(-?\d+), *(-?\d+)>, v=< *(-?\d+), *(-?\d+), *(-?\d+)>, a=< *(-?\d+), *(-?\d+), *(-?\d+)>"
)


def man_dist(v):
    return np.sum(np.abs(v))


def vel_crit(a, v):
    s = np.sign(a)
    crit = np.sum(s * v)
    crit += np.sum(np.where(a == 0, 1, 0) * np.abs(v))
    return crit


class Particles:
    def __init__(self, data):
        p = []
        v = []
        a = []
        for line in data.split("\n"):
            p.append([int(d) for d in reg.match(line).group(1, 2, 3)])
            v.append([int(d) for d in reg.match(line).group(4, 5, 6)])
            a.append([int(d) for d in reg.match(line).group(7, 8, 9)])
        self.n = len(a)
        self.p = np.array(p, dtype=int)
        self.v = np.array(v, dtype=int)
        self.a = np.array(a, dtype=int)

    def step(self):
        self.v += self.a
        self.p += self.v

    def resolve_col(self):
        index = np.full(self.n, fill_value=False, dtype=bool)
        for i in range(1, self.n):
            idx = np.r_[i : self.n, 0:i]
            collision = np.all(self.p == self.p[idx], axis=1)
            index = np.logical_or(index, collision)
        self.p = self.p[~index]
        self.v = self.v[~index]
        self.a = self.a[~index]

        self.n = np.sum(~index)

    def n_possible_collisions(self):
        possible_collisons = 0
        for i in range(1, self.n):
            idx = np.r_[i : self.n, 0:i]
            p_s = self.p < self.p[idx]
            v_s = self.v <= self.v[idx]
            a_s = self.a <= self.a[idx]
            left_not_collision = np.stack((p_s, v_s, a_s), axis=-1)
            left_not_collision = np.all(left_not_collision, axis=2)
            left_not_collision = np.any(left_not_collision, axis=1)

            p_s = self.p > self.p[idx]
            v_s = self.v >= self.v[idx]
            a_s = self.a >= self.a[idx]
            right_not_collision = np.stack((p_s, v_s, a_s), axis=-1)
            right_not_collision = np.all(right_not_collision, axis=2)
            right_not_collision = np.any(right_not_collision, axis=1)

            not_collision = np.logical_or(left_not_collision, right_not_collision)
            possible_collisons += np.sum(~not_collision)
        return possible_collisons

    def evolve_until_collisions(self):
        self.resolve_col()
        while self.n_possible_collisions() > 0:
            self.step()
            self.resolve_col()

    def find_closest_particle(self):
        min_ind = 0
        min_a = man_dist(self.a[0])
        min_v = vel_crit(self.a[0], self.v[0])
        for i in range(1, self.n):
            a_norm = man_dist(self.a[i])
            v_crit = vel_crit(self.a[i], self.v[i])
            if (a_norm < min_a) or ((a_norm == min_a) and (v_crit < min_v)):
                min_a = a_norm
                min_v = v_crit
                min_ind = i
                duplicate_min = 1
            elif (a_norm == min_a) and (v_crit == min_v):
                duplicate_min += 1
        if duplicate_min > 1:
            raise RuntimeError("Unable to find a unique minimum")
        return min_ind


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    par = Particles(data)
    print("Part 1")
    print(
        f"The {par.find_closest_particle()}th particle will stay closest to <0,0,0> in the long term"
    )
    print()

    print("Part 2")
    par.evolve_until_collisions()
    print(f"{par.n} particles remain after all collisions are resolved")


if __name__ == "__main__":
    main()
