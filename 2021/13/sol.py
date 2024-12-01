from pathlib import Path
import parse
import numpy as np

data_folder = Path(".").resolve()


def parse_data(data):
    dots, instrs_raw = data.split("\n\n")
    dots = np.array([eval(line) for line in dots.split("\n")])
    dots = dots[:, [1, 0]]
    dim = np.max(dots, axis=0)
    paper = np.full(dim + 1, fill_value=False, dtype=bool)
    paper[dots[:, 0], dots[:, 1]] = 1

    parse_instrs = parse.compile("fold along {}={}")
    instrs = []
    for line in instrs_raw.split("\n"):
        raw = parse_instrs.parse(line).fixed
        instrs.append([raw[0], int(raw[1])])

    return paper, instrs


def make_fold(paper, instr):
    line = instr[1]
    if instr[0] == "x":
        new_paper = np.copy(paper[:, :line])
        fold_ind = new_paper.shape[1] - paper[:, -1:line:-1].shape[1]
        new_paper[:, fold_ind:] |= paper[:, -1:line:-1]
    else:
        new_paper = np.copy(paper[:line, :])
        fold_ind = new_paper.shape[0] - paper[-1:line:-1].shape[0]
        new_paper[fold_ind:] |= paper[-1:line:-1]
    return new_paper


def print_paper(paper):
    s = ""
    for line in paper:
        for char in line:
            s += "\u25ae" if char else " "
        s += "\n"
    print(s)


def fold_paper(paper, instrs):
    for instr in instrs:
        paper = make_fold(paper, instr)
    return paper


def main():
    data = data_folder.joinpath("input.txt").read_text()
    paper, instrs = parse_data(data)

    print("Part 1")
    folded_paper = make_fold(paper, instrs[0])
    print(f"There are {np.sum(folded_paper)} visible dots after the first fold")
    print()

    print("Part 2")
    print("After folding the paper displays the code:")
    print_paper(fold_paper(paper, instrs))
    print()


if __name__ == "__main__":
    main()
