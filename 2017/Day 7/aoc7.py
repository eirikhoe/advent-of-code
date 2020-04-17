from pathlib import Path
import re

data_folder = Path(".").resolve()
reg = re.compile(r"(\w+) \((\d+)\)(?: -> (.+))?")


class Program:
    def __init__(self, name, weight, children):
        self.name = name
        self.weight = weight
        self.children = children
        self.total_weight = 0
        self.parent = None


class Tower:
    def __init__(self, data):
        self.programs = dict()

        for line in data.split("\n"):
            m = reg.match(line)
            name = m.group(1)
            weight = int(m.group(2))
            if m.group(3) is not None:
                children = m.group(3).split(", ")
            else:
                children = []
            self.programs[name] = Program(name, weight, children)
        self.bottom = self.find_parents()
        self.find_total_weight()
        self.imbalance = None
        self.find_imbalance()

    def find_parents(self):
        all_children = []
        for name in self.programs:
            for child in self.programs[name].children:
                all_children.append(child)
                self.programs[child].parent = name

        for name in self.programs:
            if self.programs[name].children and (name not in all_children):
                return name

    def find_total_weight(self):
        name = self.bottom
        self._find_total_weight(name)

    def _find_total_weight(self, name):
        total_weight = self.programs[name].weight
        for child in self.programs[name].children:
            total_weight += self._find_total_weight(child)
        self.programs[name].total_weight = total_weight
        return total_weight

    def balanced_weight(self):
        parent = self.programs[self.imbalance].parent
        for child in self.programs[parent].children:
            if child != self.imbalance:
                return self.programs[self.imbalance].weight + (
                    self.programs[child].total_weight
                    - self.programs[self.imbalance].total_weight
                )

    def find_imbalance(self):
        self._imbalance_step(self.bottom, False)

    def _imbalance_step(self, name, suspicious):
        n_children = 0
        first_child_weight = None
        weight_groups = [[], []]
        imbalance = False
        for j, child in enumerate(self.programs[name].children):
            if first_child_weight is None:
                first_child_weight = self.programs[child].total_weight
                weight_groups[0].append(j)
            else:
                if first_child_weight != self.programs[child].total_weight:
                    weight_groups[1].append(j)
                else:
                    weight_groups[0].append(j)

            n_children += 1

        if (n_children == 0) and suspicious:
            self.imbalance = name
        elif n_children == 1:
            raise RuntimeError("Nodes with one child not allowed")
        elif n_children >= 2:
            if weight_groups[1]:
                if n_children == 2:
                    for child in self.programs[name].children:
                        self._imbalance_step(child, False)
                if n_children > 2:
                    for group in weight_groups:
                        if len(group) == 1:
                            self._imbalance_step(
                                self.programs[name].children[group[0]], True
                            )
            elif suspicious:
                self.imbalance = name


def main():
    data = data_folder.joinpath("input.txt").read_text()

    t = Tower(data)
    
    print("Part 1")
    print(f"The bottom program is {t.bottom}")
    print()

    print("Part 2")
    print(f"The inbalanced node's weight would need to be {t.balanced_weight()} to balance the entire tower")


if __name__ == "__main__":
    main()
