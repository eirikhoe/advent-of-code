import numpy as np

module_masses = []
with open("input.txt", "r") as file:
    module_masses = np.array([int(line.rstrip()) for line in file])

total_fuel_required = np.sum(module_masses // 3 - 2)
