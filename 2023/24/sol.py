from pathlib import Path
import random
import copy

data_folder = Path(".").resolve()


def update_pos(pos, dir, step):
    return tuple([pos[k] + step * dir[k] for k, _ in enumerate(pos)])


def parse_data(data):
    particles = []
    for line in data.split("\n"):
        x, v = line.split(" @ ")
        x = tuple(int(d) for d in x.split(", "))
        v = tuple(int(d) for d in v.split(", "))
        particles.append((x, v))
    return particles


def dot(x, y):
    return sum([x[i] * y[i] for i, _ in enumerate(x)])


def check_colision(first, second, lim):
    x1, v1 = first
    x2, v2 = second
    x2 = x2[:2]
    x1 = x1[:2]
    v1 = v1[:2]
    v2 = v2[:2]
    dot_prod = dot(v1, v2)
    # parallel
    if dot_prod**2 == dot(v1, v1) * dot(v2, v2):
        return False
    if (max(v1) == 0) or (max(v2) == 0):
        if all([x1[i] == x2[i] for i in range(2)]):
            return x1
        return False

    r = [0, 1]
    b = [x1[i] - x2[i] for i in range(2)]
    a = [[v2[i], -v1[i]] for i in range(2)]
    if a[0][0] == 0:
        r = [1, 0]

    k = a[r[1]][0] / a[r[0]][0]
    sol = [None for i in range(2)]
    sol[r[1]] = (b[r[1]] - k * b[r[0]]) / (a[r[1]][1] - k * a[r[0]][1])
    sol[r[0]] = (b[r[0]] - a[r[0]][1] * sol[r[1]]) / a[r[0]][0]
    if min(sol) < 0:
        return False
    col_point = update_pos(x1, v1, sol[1])
    return all((lim[0] <= col_point[i] <= lim[1]) for i in range(2))


def count_intersections(particles, lim):
    n_intersections = 0
    for i in range(len(particles) - 1):
        for j in range(i + 1, len(particles)):
            n_intersections += int(check_colision(particles[i], particles[j], lim))
    return n_intersections


def get_pos(particle, t):
    return update_pos(particle[0], particle[1], t)


def min_func(particles, x):
    n = len(particles)
    times = x[:n]
    throw = x[n:]
    val = 0
    for i, p in enumerate(particles):
        for j in range(3):
            val += (p[0][j] - throw[j] + times[i] * (p[1][j] - throw[j + 3])) ** 2
    return val


def gradient(particles, x):
    grad = [0 for _ in range(6)]
    n = len(particles)
    times = x[:n]
    throw = x[n:]
    for i, p in enumerate(particles):
        for j in range(3):
            g = p[0][j] - throw[j] + times[i] * (p[1][j] - throw[j + 3])
            grad[j] += -2 * g
            grad[j + 3] += -2 * times[i] * g
    return grad


def scale_particles(particles, scale, inv):
    if inv:
        scale = [1 / s for s in scale]
    particles = copy.deepcopy(particles)
    scaled = [None for _ in range(2)]
    for i, _ in enumerate(particles):
        for k in range(2):
            scaled[k] = tuple(particles[i][k][j] * scale[k] for j in range(3))
        particles[i] = tuple(scaled)
    return particles


def scale_x(x, scale):
    x = copy.deepcopy(x)
    n = len(x)
    scale_t = scale[0] / scale[1]
    for i in range(n - 6):
        x[i] = round(x[i] * scale_t)
    for i in range(n - 6, n - 3):
        x[i] = round(x[i] * scale[0])
    for i in range(n - 3, n):
        x[i] = round(x[i] * scale[1])
    return x


def get_scale(particles):
    scale = [0, 0]
    for _, particle in enumerate(particles):
        for j, _ in enumerate(particle[0]):
            for k in range(2):
                val = abs(particle[k][j])
                if val > scale[k]:
                    scale[k] = val
    return scale


def get_lims(particles):
    lims = [[], []]
    for i in range(3):
        for k in range(2):
            lims[k].append([0, 0])
            lims[k][i][0] = min([p[k][i] for p in particles])
            lims[k][i][1] = max([p[k][i] for p in particles])
    return lims


def get_random_init_value(particles, lims):
    n = len(particles)
    x = [0 for _ in range(n + 6)]
    sides = [random.randrange(2) for _ in range(3)]
    for j in range(3):
        for k in range(2):
            d = lims[k][j][1] - lims[k][j][0]
            if sides[j] == 1 - k:
                x[n + j + 3 * k] = random.uniform(lims[k][j][0] - d, lims[k][j][0])
            else:
                x[n + j + 3 * k] = random.uniform(lims[k][j][1], lims[k][j][1] + d)
    for i in range(n):
        x[i] = find_min_t(particles[i], x[-6:])
    return x


def nudge(x, particles):
    min_val = min_func(particles, x)
    n = len(x) - 6
    best = x
    change = True
    while change:
        change = False
        for j in range(6):
            for dir in [-1, 1]:
                x = copy.deepcopy(best)
                x[n + j] += dir
                for i in range(n):
                    x[i] = round(find_min_t(particles[i], x[-6:]))
                val = min_func(particles, x)
                if val < min_val:
                    best = x
                    min_val = val
                    change = True
    return best


def find_throw(particles):
    scale = get_scale(particles)
    particles = scale_particles(particles, scale, True)
    lims = get_lims(particles)
    min_val = None
    for _ in range(100_000):
        x_cand = get_random_init_value(particles, lims)
        val = min_func(particles, x_cand)
        if (min_val is None) or (val < min_val):
            x = x_cand
            min_val = val
    x = gradient_descent(particles, x, scale)
    particles = scale_particles(particles, scale, False)
    return nudge(x, particles)[-6:]


def gradient_descent(particles, x, scale):
    j = 0
    k = len(particles)
    old_scaled = scale_x(x, scale)
    old_min = min_func(particles, x)
    while True:
        grad = gradient(particles, x)
        x[-6:] = [x[i + k] - 0.002 * grad[i] for i in range(6)]
        for i in range(k):
            x[i] = find_min_t(particles[i], x[-6:])
        j += 1
        if (j % 1000) == 0:
            scaled = scale_x(x, scale)
            min_val = min_func(particles, x)
            if all([old_scaled[i] == scaled[i] for i, _ in enumerate(scaled)]) and (
                min_val >= old_min
            ):
                return scaled
            old_scaled = scaled
            old_min = min_val


def find_min_t(particle, throw):
    num = 0
    denom = 0
    for j, _ in enumerate(particle[0]):
        dv = particle[1][j] - throw[j + 3]
        dx = particle[0][j] - throw[j]
        num += dx * dv
        denom += dv**2
    return -num / denom


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    particles = parse_data(data)

    print("Part 1")
    lim = [200000000000000, 400000000000000]  # For the real input
    # lim = [7,27] # For the example input
    n_intersections = count_intersections(particles, lim)
    print(f"There are {n_intersections} intersections in the target area.")
    print()

    print("Part 2")
    throw = find_throw(particles)
    print(f"The sum of the coordinates of the perfect throw is {sum(throw[:3])}.")
    print()


if __name__ == "__main__":
    main()
