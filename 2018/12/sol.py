from pathlib import Path
import numpy as np
import re
from bisect import bisect_left
def main():
    data_folder = Path(".").resolve()
    text = data_folder.joinpath("input.txt").read_text().split("\n")
    
    cave = Cave(text)
    n_gen = 20
    print(f"Sum of plant locations after {n_gen} generations: {cave.find_plant_sum(n_gen)}")
    n_gen = int(5e10)
    print(f"Sum of plant locations after {n_gen} generations: {cave.find_plant_sum(n_gen)}")

class Cave():
    rule_reg = re.compile(r"([#.]{5}) => #")
    
    def __init__(self,desc):
        init_state = desc[0][15:]
        self.init_plants = []
        for i,pot in enumerate(init_state):
            if pot == "#":
                self.init_plants.append(i)
        
        self.plant_criteria = []

        for line in desc[2:]:
            m = Cave.rule_reg.match(line)
            if m:
                rule = m.group(1)
                rule_int = 0
                for i,char in enumerate(rule):
                    if char == "#":
                        rule_int += 2**i
                self.plant_criteria.append(rule_int)
        self.plant_criteria.sort()

    def evolve(self,t,full=False):
        plants = self.init_plants
        evolution = [plants]
        for i in range(t):
            plants = self.step(plants)
            if full:
                evolution.append(plants)
        if full:
            return evolution
        else:
            return plants
    
    def find_plant_sum(self,t):
        plants  = self.init_plants
        aborted = False
        for i in range(t):
            new_plants = self.step(plants)
            if len(new_plants)==len(plants):
                diff = new_plants[0]-plants[0]
                eq = True
                for j in range(1,len(plants)):
                    if (new_plants[j]-plants[j]) != diff:
                        eq=False
                        break
                if eq:
                    aborted = True
                    break
            plants = new_plants

        if aborted:
            return sum(plants)+len(plants)*diff*(t-i)
        else:
            return sum(new_plants)
                

    def step(self,plants):
        plants_new = []
        for loc in range(plants[0]-2,plants[-1]+3):
            loc_int = 0
            for i,rel_loc in enumerate(range(loc-2,loc+3)):
                ind = bisect_left(plants,rel_loc)
                if (ind < len(plants)) and (plants[ind]==rel_loc):
                    loc_int += 2**i
            ind = bisect_left(self.plant_criteria,loc_int)
            if (ind < len(self.plant_criteria)) and (self.plant_criteria[ind]==loc_int):
                plants_new.append(loc)
        return plants_new
            


    

    def print_plants(self,t,t_start=0):
        evolution = self.evolve(t,True)
        evolution = evolution[t_start:]
        lims = [evolution[0][0],evolution[0][-1]]
        for state in evolution[1:]:
            if state[0] < lims[0]:
                lims[0] = state[0]
            if state[-1] > lims[1]:
                lims[1] = state[-1]
        s = ""
        len_size = max(len(str(lims[0])),len(str(lims[1])))
        form_str = "{:" + str(len_size) + "d}"
        for j in range(len_size):
            s += "   "
            for loc in range(lims[0],lims[1]+1):
                if loc % 10 == 0:
                    loc_str = form_str.format(loc)
                    s += loc_str[j]
                else:
                    s += " "
            s += "\n"

        state_size = max(len(str(t_start)),len(str(t)))
        form_str = "{:" + str(state_size) + "d}"
        for i,state in enumerate(evolution):
            s += form_str.format(i+t_start) + ": "
            for loc in range(lims[0],lims[1]+1):
                ind = bisect_left(state,loc)
                if (ind < len(state)) and (state[ind]==loc):
                    s += "#"
                else:
                    s += "."
            s += "\n"
        print(s)               


if __name__ == "__main__":
    main()