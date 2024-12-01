from pathlib import Path
from math import prod


def operate(a, op, b):
    if op == "+":
        return a + b
    elif op == "*":
        return a * b
    else:
        raise RuntimeError("Invalid operator")


def evaluate_eq_pres(equation):
    levels = [[0, "+"]]

    for term in equation:
        if term == "(":
            levels.append([0, "+"])
        elif term == ")":
            res = levels.pop()[0]
            levels[-1][0] = operate(*levels[-1], res)
        elif term in ["*", "+"]:
            levels[-1][1] = term
        else:
            num = int(term)
            levels[-1][0] = operate(*levels[-1], num)
    return levels[0][0]


def evaluate_add_first(equation):
    levels = [[0]]
    for term in equation:
        if term == "(":
            levels.append([0])
        elif term == ")":
            terms = levels.pop()
            res = prod(terms)
            levels[-1][-1] += res
        elif term == "*":
            levels[-1].append(0)
        elif term != "+":
            num = int(term)
            levels[-1][-1] += num

    return prod(levels[0])


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    equations = [
        eq.replace("(", "( ").replace(")", " )").split() for eq in data.split("\n")
    ]

    print("Part 1")
    total = 0
    for equation in equations:
        total += evaluate_eq_pres(equation)
    print("Evaluating the expression on each line of the homework ")
    print("with equal operator presedence, the sum of the ")
    print(f"resulting values is {total}")
    print()

    print("Part 2")
    total = 0
    for equation in equations:
        total += evaluate_add_first(equation)
    print("Evaluating the expression on each line of the homework ")
    print("with addition evaluated before multiplication, the sum ")
    print(f"of the resulting values is {total}")


if __name__ == "__main__":
    main()
