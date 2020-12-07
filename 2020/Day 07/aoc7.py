from collections import defaultdict
from collections import deque
from copy import deepcopy
from pathlib import Path
import re

re_bags_parent = re.compile(r"(\w+ \w+) bags contain")
re_bags_children = re.compile(r"(\d+) (\w+ \w+) bags?[.,]")


class Bags:
    def __init__(self, bag_data):
        self.children = dict()
        self.parents = defaultdict(list)
        for line in bag_data.split("\n"):
            m = re_bags_parent.match(line)
            if not m:
                raise RuntimeError("Invalid data")
            parent = m.groups()[0]
            chd = re_bags_children.findall(line)
            self.children[parent] = [[int(c[0]), c[1]] for c in chd]
            for c in chd:
                self.parents[c[1]].append(parent)
        self.bag_colors = set(self.parents.keys()) | set(self.children.keys())

    def find_all_parents(self, bag_color):
        if bag_color not in self.bag_colors:
            raise RuntimeError("Invalid bag color")
        parents = set(self.parents[bag_color])
        candidates = deque(parents)
        while candidates:
            candidate = candidates.pop()
            candidate_parents = self.parents[candidate]
            for candidate_parent in candidate_parents:
                if candidate_parent not in parents:
                    candidates.appendleft(candidate_parent)
                    parents.add(candidate_parent)
        return list(parents)

    def count_bags_inside(self, bag_color):
        try:
            children = self.children[bag_color]
        except KeyError:
            raise RuntimeError("Invalid bag color")
        n_bags = 0
        candidates = deque(children)
        while candidates:
            candidate = candidates.pop()
            candidate_children = deepcopy(self.children[candidate[1]])
            for candidate_child in candidate_children:
                candidate_child[0] *= candidate[0]
                candidates.appendleft(candidate_child)
            n_bags += candidate[0]
        return n_bags


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    b = Bags(data)
    bag_color = "shiny gold"
    n_bags = len(b.find_all_parents(bag_color))
    print("Part 1")
    print("The number of bag colors that can eventually contain")
    print(f"at least one {bag_color} bag is {n_bags}")
    print()

    n_bags = b.count_bags_inside("shiny gold")
    print("Part 2")
    print(f"{n_bags} individual bags are required inside your single {bag_color} bag")


if __name__ == "__main__":
    main()
