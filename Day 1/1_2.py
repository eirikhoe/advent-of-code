import numpy as np

current_masses = []
with open('day_1_input.txt','r') as file:
    current_masses = np.array([int(line.rstrip()) for line in file])

fuel_required = np.zeros(current_masses.shape,dtype=int)
while np.max(current_masses) > 8: 
    current_masses = np.where(current_masses > 8, current_masses//3 - 2,0)
    fuel_required += current_masses

total_fuel_required = np.sum(fuel_required)