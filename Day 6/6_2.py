import numpy as np 

orbits = dict()
with open("day_6_input.txt", "r") as file:
    for line in file:
        temp = (line.strip().split(")"))
        orbits[temp[1]] = temp[0]        

ancestors_you = []
curr_obj = 'YOU'
while curr_obj != 'COM':
    curr_obj = orbits[curr_obj]
    ancestors_you.append(curr_obj)

ancestors_san = []
curr_obj = 'SAN'
while curr_obj != 'COM':
    curr_obj = orbits[curr_obj]
    ancestors_san.append(curr_obj)

for i,ancestor in enumerate(ancestors_you):
    if ancestor in ancestors_san:
        first_common_ancestor = ancestor
        break

n_you = ancestors_you.index(first_common_ancestor)
n_san = ancestors_san.index(first_common_ancestor)

print(n_you + n_san) 