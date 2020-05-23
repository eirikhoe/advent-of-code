from pathlib import Path
import re

data_folder = Path(".").resolve()

reg = re.compile(r"\s+(\d+)")


def validate_triangle(triangle):
    triangle = sorted(triangle)
    if triangle[2] < (triangle[0] + triangle[1]):
        return True
    else:
        return False

def n_possible_triangles(triangles, rowwise=True):
    n_possible = 0
    if rowwise:
        for triangle in triangles:
            n_possible += int(validate_triangle(triangle))
    else:
        for i in range(len(triangles[0])):
            for j in range(0,len(triangles),3):
                triangle = [triangles[j][i], triangles[j + 1][i], triangles[j + 2][i]]
                n_possible += int(validate_triangle(triangle))
                
    return n_possible


def main():
    data = data_folder.joinpath("input.txt").read_text()
    lines = data.split("\n")
    triangles = []
    for line in lines:
        m = reg.findall(line)
        triangles.append([int(side) for side in m])

    print("Part 1")
    print(f"There are {n_possible_triangles(triangles)} possible triangles")
    print()

    print("Part 2")
    print(f"Reading by columns there are {n_possible_triangles(triangles,False)} possible triangles")

if __name__ == "__main__":
    main()
