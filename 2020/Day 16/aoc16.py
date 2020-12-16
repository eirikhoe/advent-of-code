from pathlib import Path
import re
import numpy as np

rule_re = re.compile("((?:[a-z] ?)+): (\d+)-(\d+) or (\d+)-(\d+)")


class Tickets:
    def __init__(self, data):
        self.rules = []
        lines = data.split("\n")
        i = 0
        while lines[i] != "":
            m = rule_re.match(lines[i])
            if m is None:
                raise RuntimeError("Invalid rule input")
            g = m.groups()
            self.rules.append(
                [g[0], [int(g[1]), int(g[2])], [int(g[3]), int(g[4])]]
            )
            i += 1
        i += 2
        self.mine = [int(d) for d in lines[i].split(",")]
        i += 3
        self.nearby = [
            [int(d) for d in line.split(",")] for line in lines[i:]
        ]
        self._possible_categories = None
        self.error_rate = self._discard_invalid_and_return_error_rate()
        self.categories = self._find_categories()

    def _discard_invalid_and_return_error_rate(self):
        valid_tickets = []
        error_rate = 0
        for ticket in self.nearby:
            valid_ticket = True
            for digit in ticket:
                invalid_digit = True
                for rule in self.rules:
                    if (rule[1][0] <= digit <= rule[1][1]) or (
                        rule[2][0] <= digit <= rule[2][1]
                    ):
                        invalid_digit = False
                        break
                if invalid_digit:
                    error_rate += digit
                    valid_ticket = False
            if valid_ticket:
                valid_tickets.append(ticket)
        self.nearby = valid_tickets
        return error_rate

    def _find_categories(self):
        valid_tickets = self.nearby + [self.mine]
        columns = list(zip(*valid_tickets))
        possible_categories = []
        for col in columns:
            possible_categories.append([])
            for rule in self.rules:
                possible_cat = True
                for digit in col:
                    if not (
                        (rule[1][0] <= digit <= rule[1][1])
                        or (rule[2][0] <= digit <= rule[2][1])
                    ):
                        possible_cat = False
                        break
                if possible_cat:
                    possible_categories[-1].append(rule[0])

        cat_lengths = [len(cat) for cat in possible_categories]
        sorted_index = np.argsort(cat_lengths)
        self._possible_categories = [
            possible_categories[s] for s in sorted_index
        ]

        assigned = []
        sorted_categories = self._assign_category(assigned)

        categories = sorted_categories.copy()
        for i, _ in enumerate(categories):
            categories[sorted_index[i]] = sorted_categories[i]
        
        return categories

    def find_departure_prod(self): 
        departure_prod = 1
        for i, _ in enumerate(self.categories):
            if self.categories[i].startswith("departure"):
                departure_prod *= self.mine[i]
        return departure_prod

    def _assign_category(self, assigned):
        n_assigned = len(assigned)
        if n_assigned == len(self._possible_categories):
            return assigned
        for possible in self._possible_categories[n_assigned]:
            if possible not in assigned:
                candidate = assigned.copy()
                candidate.append(possible)
                final = self._assign_category(candidate)
                if final is not None:
                    return final
        return None


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    t = Tickets(data)

    print("Part 1")
    print(f"The scanning error rate is {t.error_rate}")
    print()

    print("Part 2")
    departure_prod = t.find_departure_prod()
    print("The product of the six departure fields on the ")
    print(f"ticket is {departure_prod}")

if __name__ == "__main__":
    main()
