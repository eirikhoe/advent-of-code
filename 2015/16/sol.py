from pathlib import Path
import re

data_folder = Path(__file__).parent.resolve()

reg_aunt = re.compile(r"Sue (\d+): (.+)")


def find_aunt(data, corrected=False):
    target = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }
    less_than_properties = ["pomeranians", "goldfish"]
    greater_than_properties = ["cats", "trees"]

    aunt_candidates = []
    for line in data.split("\n"):
        m = reg_aunt.match(line)
        assert m is not None
        info = m.group(2).split(", ")
        info = [d.split(": ") for d in info]
        property_names = [d[0] for d in info]
        properties = [int(d[1]) for d in info]
        property_dict = dict(zip(property_names, properties))
        right_aunt = True
        for property in property_dict:
            if corrected:
                if property in greater_than_properties:
                    right_aunt = property_dict[property] > target[property]
                elif property in less_than_properties:
                    right_aunt = property_dict[property] < target[property]
                else:
                    right_aunt = property_dict[property] == target[property]
            else:
                right_aunt = property_dict[property] == target[property]

            if not right_aunt:
                break

        if right_aunt:
            aunt_candidates.append(m.group(1))

    if len(aunt_candidates) == 0:
        return None
    elif len(aunt_candidates) > 1:
        raise RuntimeWarning("Multiple aunt candidates found")
        return aunt_candidates
    else:
        return aunt_candidates[0]


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    print("Part 1")
    print(f"Sue {find_aunt(data)} sent me the gift")
    print()

    print("Part 2")
    print(f"Sue {find_aunt(data,True)} sent me the gift")


if __name__ == "__main__":
    main()
