from pathlib import Path
import numpy as np
import parse

data_folder = Path(".").resolve()


def parse_data(data):
    alg, image = data.split("\n\n")
    alg = [True if c == "#" else False for c in alg]
    odd = set()
    for i, line in enumerate(image.split("\n")):
        for j, char in enumerate(line):
            if char == "#":
                odd.add((i, j))
    dim = find_dim(odd)
    return alg, odd, False, dim


def enhance_pixel(pos, odd, alg, odd_not_lit):
    bin = ""
    for i in range(-1, 2):
        for j in range(-1, 2):
            bin += "1" if ((pos[0] + i, pos[1] + j) in odd) ^ odd_not_lit else "0"
    ind = int(bin, 2)
    return alg[ind] ^ odd_not_lit


def enhance_image(odd, alg, odd_not_lit, dim, n_steps):
    odd = odd.copy()
    for _ in range(n_steps):
        odd, odd_not_lit, dim = enhance_image_step(odd, alg, odd_not_lit, dim)
    return odd


def enhance_image_step(odd, alg, odd_not_lit, dim):
    old_odd = odd
    odd = set()
    for i in range(dim[0][0] - 1, dim[0][1] + 2):
        for j in range(dim[1][0] - 1, dim[1][1] + 2):
            if enhance_pixel((i, j), old_odd, alg, odd_not_lit):
                odd.add((i, j))

    if ((not odd_not_lit) and alg[0]) or (odd_not_lit and (not alg[-1])):
        odd_not_lit = not odd_not_lit
        new_odd = set()
        for i in range(dim[0][0] - 1, dim[0][1] + 2):
            for j in range(dim[1][0] - 1, dim[1][1] + 2):
                if (i, j) not in odd:
                    new_odd.add((i, j))
        odd = new_odd
    dim = find_dim(odd)
    return odd, odd_not_lit, dim


def find_dim(odd):
    dim = [[None, None], [None, None]]
    dim[0][0] = min([p[0] for p in odd])
    dim[0][1] = max([p[0] for p in odd])
    dim[1][0] = min([p[1] for p in odd])
    dim[1][1] = max([p[1] for p in odd])
    return dim


def print_image(odd, odd_not_lit, dim, ending=""):
    s = ""
    for i in range(dim[0][0] - 1, dim[0][1] + 2):
        for j in range(dim[1][0] - 1, dim[1][1] + 2):
            if ((i, j) in odd) ^ odd_not_lit:
                s += "#"
            else:
                s += "."
        s += "\n"
    data_folder.joinpath(f"image{ending}.txt").write_text(s)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    alg, odd, odd_not_lit, dim = parse_data(data)

    print("Part 1")
    n = 2
    odd_enhanced = enhance_image(odd, alg, odd_not_lit, dim, n)
    n_lit_pixels = len(odd_enhanced) if (n % 2 == 0) else "infinite"
    print(f"After {n} enhancements {n_lit_pixels} pixels are lit")

    print()

    print("Part 2")
    n = 50
    odd_enhanced = enhance_image(odd, alg, odd_not_lit, dim, n)
    n_lit_pixels = len(odd_enhanced) if (n % 2 == 0) else "infinite"
    print(f"After {n} enhancements {len(odd_enhanced)} pixels are lit")
    print()


if __name__ == "__main__":
    main()
