import numpy as np 

orbits = dict()
with open("day_6_input.txt", "r") as file:
    for line in file:
        temp = (line.strip().split(")"))
        orbits[temp[1]] = temp[0]        
n = 0
for key in orbits:
    curr_obj = key
    while curr_obj != 'COM':
        curr_obj = orbits[curr_obj]
        n +=1

print(n) 