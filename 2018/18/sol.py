from pathlib import Path
import numpy as np
import re
from bisect import bisect_left
from copy import deepcopy
from itertools import compress

def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    
    print("Part 1:")
    f = Forest(data)
    n_minutes = 10
    print(f"The total resource value is {f.resource_value(n_minutes)} after {n_minutes} minute{'s' if n_minutes > 0 else ''}.")
    print()

    print('Part 2:')
    f = Forest(data)
    n_minutes = 1000000000
    print(f"The total resource value is {f.resource_value(n_minutes)} after {n_minutes} minute{'s' if n_minutes > 0 else ''}.")
    
class Forest():

    def __init__(self,data):
        self.ground = [list(line) for line in data.split("\n")]    
        self.dim = [len(self.ground),len(self.ground[0])]
    def _adj_acres(self,y,x):
        adj_coords = [[y-1,x-1],
                      [y-1,x],
                      [y-1,x+1],
                      [y,x-1],
                      [y,x+1],
                      [y+1,x-1],
                      [y+1,x],
                      [y+1,x+1]]
        adj_acres = []
        for coord in adj_coords:
            if (0<= coord[0] < self.dim[0]) and (0<= coord[1] < self.dim[1]):
                adj_acres.append(self.ground[coord[0]][coord[1]])
        
        return adj_acres

    def step(self):
        new_ground = deepcopy(self.ground)
        for y in range(self.dim[0]):
            for x in range(self.dim[1]):
                new_ground[y][x] = self._find_acre_type(y,x)
        self.ground = new_ground

    def evolve(self,t,print_forest=False):
        if print_forest:
            print("Initial state:")
            self.print_ground()
            print()
        for i in range(t):
            self.step()
            if print_forest:
                print(f"After {i+1} minute{'s' if i > 0 else ''}:")
                self.print_ground()
                print()

    def _find_acre_type(self,y,x):
        adj_acres = self._adj_acres(y,x)
        if self.ground[y][x] == '.':
            tree_count = 0
            for adj_acre in adj_acres:
                tree_count += int(adj_acre=='|')
            if tree_count >= 3:
                return '|'
            else:
                return '.'
        elif self.ground[y][x] == '|':
            lumberyard_count = 0
            for adj_acre in adj_acres:
                lumberyard_count += int(adj_acre=='#')
            if lumberyard_count >= 3:
                return '#'
            else:
                return '|'
        elif self.ground[y][x] == '#':
            tree_count = 0
            lumberyard_count = 0
            for adj_acre in adj_acres:
                tree_count += int(adj_acre=='|')
                lumberyard_count += int(adj_acre=='#')
            if (tree_count == 0) or (lumberyard_count == 0):
                return '.'
            else:
                return '#'

    def resource_value(self,t):
        
        previous_states = [deepcopy(self.ground)]
        i = 0
        cycle = None
        while (cycle is None) and (i < t):
            self.step()
            curr_state = deepcopy(self.ground)
            i += 1
            for k,state in enumerate(previous_states):
                match = True
                for y in range(self.dim[0]):
                    for x in range(self.dim[1]):
                        if state[y][x] != curr_state[y][x]:
                            match = False
                            break
                    if not match:
                        break
                if match:
                    cycle = [k,i]
                    break
            previous_states.append(curr_state)

        if i == t:
            state = curr_state
        elif cycle is not None:
            new_t = cycle[0] + ((t-cycle[0]) % (cycle[1]-cycle[0]))
            state = previous_states[new_t]
        tree_count = 0
        lumberyard_count = 0
        for y in range(self.dim[0]):
            for acre in state[y]:
                tree_count += int(acre=='|')
                lumberyard_count += int(acre=='#')
        return tree_count*lumberyard_count

    def print_ground(self,ret=False):
        line = []
        for y in range(self.dim[0]):
            s = ""
            for k in self.ground[y]:
                s += k   
            line.append(s)
        output = '\n'.join(line)
        if ret:
            return output
        else:
            print(output)
if __name__ == "__main__":
    main()