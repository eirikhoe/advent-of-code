from pathlib import Path
import numpy as np
import re


def find_all(sub, a_str):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += 1


def gen_molecule(reactions, molecule):
    n_m = len(molecule)
    molecule_list = list(molecule)
    unique_mols = set()
    for reaction in reactions:
        n_r = len(reaction[0])
        n_p = len(reaction[1])
        result_len = n_m + (n_p - n_r)
        if result_len <= 0:
            continue
        result = np.full(n_m + (n_p - n_r), "a", dtype=object)
        for match in find_all(reaction[0], molecule):
            result[:match] = molecule_list[:match]
            result[match : match + n_p] = list(reaction[1])
            result[match + n_p :] = molecule_list[match + n_r :]
            result_str = "".join(list(result))
            unique_mols.add(result_str)

    unique_mols = list(unique_mols)
    return unique_mols


def count_evolutions(reactions, molecule):
    return len(gen_molecule(reactions, molecule))


def steps_to_molecule(molecule):
    """
    Use that every reaction is of one of two forms
    1. X -> XX (or e -> XX)
    2. X -> XRn(XY)*XAr
    ( )* denotes 0 or more of the expression inside the parenthesis
    X denotes any element not equal to Rn, Y or Ar
    """

    reg_mol = re.compile(r"[A-Z][a-z]?")
    molecule = reg_mol.findall(molecule)
    steps = 0
    while "Ar" in molecule:
        end_ind = molecule.index("Ar")
        start_ind = end_ind - molecule[end_ind::-1].index("Rn")
        assert molecule[start_ind - 1] not in ["Rn", "Ar", "Y"]
        index = start_ind
        for i in range(start_ind + 1, end_ind):
            if molecule[i] == "Y":
                assert i > index + 1
                steps += i - index - 2
                index = i

        assert end_ind > index + 1
        steps += end_ind - index - 2

        molecule = molecule[:start_ind] + molecule[(end_ind + 1) :]
        steps += 1

    return steps + len(molecule) - 1


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    data = data.split("\n")
    molecule = data[-1]
    reactions = [reaction.split(" => ") for reaction in data[:-2]]
    n_molecules = count_evolutions(reactions, molecule)

    print("Part 1")
    print(f"{n_molecules} distinct molecules can be created")
    print()

    print("Part 2")
    print(f"It takes {steps_to_molecule(molecule)} steps to make the medicine")


if __name__ == "__main__":
    main()
