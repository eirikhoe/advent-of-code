def find_ancestor_list(obj):
    ancestors = []
    while obj != "COM":
        obj = orbits[obj]
        ancestors.append(obj)
    return ancestors


orbits = dict()
with open("day_6_input.txt", "r") as file:
    for line in file:
        objcts = line.strip().split(")")
        orbits[objcts[1]] = objcts[0]

ancestors_you = find_ancestor_list("YOU")
ancestors_san = find_ancestor_list("SAN")

for i, ancestor in enumerate(ancestors_you):
    if ancestor in ancestors_san:
        first_common_ancestor = ancestor
        break

n_you = ancestors_you.index(first_common_ancestor)
n_san = ancestors_san.index(first_common_ancestor)

print(n_you + n_san)

