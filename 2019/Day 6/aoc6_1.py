orbits = dict()
with open("day_6_input.txt", "r") as file:
    for line in file:
        objcts = line.strip().split(")")
        orbits[objcts[1]] = objcts[0]
n_orbits = 0
for key in orbits:
    curr_obj = key
    while curr_obj != "COM":
        curr_obj = orbits[curr_obj]
        n_orbits += 1

print(n_orbits)

