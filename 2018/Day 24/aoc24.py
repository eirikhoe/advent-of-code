
from pathlib import Path
import numpy as np
import re
from collections import deque
data_folder = Path(".").resolve()

reg_main = re.compile(r"(\d+) units each with (\d+) hit points(?: \((.+)\))* with an attack that does (\d+) (\w+) damage at initiative (\d+)")
reg_immune = re.compile(r"immune to (\w+(?:, \w+)*)")
reg_weak = re.compile(r"weak to (\w+(?:, \w+)*)")

class Disease:

    def __init__(self,data,boost=0):
        
        self.n_units = []
        self.hp = []
        self.ap = []
        self.initiative = []
        self.weakness = []
        self.immune = []
        self.attack_type = []
        self.ep = []
        self.n_defenders = 0
        self.target = []
        self.targeted = []
        added_defenders = 1
        group_id = 1
        self.group_ids = []
        self.possible_targets = []
        self.kills = []
        self.winner = None
        for line in data.split('\n'):
            if line == "Infection:":
                added_defenders = 0
                group_id = 1
            m = reg_main.match(line)
            if m:
                self.n_units.append(int(m.group(1)))
                self.hp.append(int(m.group(2)))
                if m.group(3) is not None:

                    weaknesses = reg_weak.search(m.group(3))
                    if weaknesses:
                        self.weakness.append(weaknesses.group(1).split(", "))
                    else:
                        self.weakness.append([])

                    immunities = reg_immune.search(m.group(3))
                    if immunities:
                        self.immune.append(immunities.group(1).split(", "))
                    else:
                        self.immune.append([])
                else:
                    self.weakness.append([])
                    self.immune.append([])

                self.ap.append(int(m.group(4)) + added_defenders*boost)
                self.attack_type.append(m.group(5))
                self.initiative.append(int(m.group(6)))

                self.ep.append(self.n_units[-1]*self.ap[-1])
                self.target.append(None)
                self.targeted.append(False)
                self.group_ids.append(group_id)
                group_id += 1
                self.n_defenders += added_defenders
                self.possible_targets.append([]) 
                self.kills.append(0)


    def target_selection(self):
        selection_order = np.lexsort((self.initiative,self.ep))[::-1]
        for group in selection_order:
            self.find_target(group)
        

    def attack(self):
        attack_order = np.argsort(self.initiative)[::-1]
        attackers = []
        for attacker in attack_order:
            target = self.target[attacker]
            if (target is not None) and (self.n_units[attacker] > 0):
                damage = self.get_damage(attacker,target)
                units_killed = min(damage//self.hp[target],self.n_units[target])
                self.n_units[target] -= units_killed
                self.ep[target] -= units_killed*self.ap[target]
                attackers.append(attacker)
            else:
                units_killed = 0
            self.kills[attacker] = units_killed
        
        return attackers
    
    def cleanup(self):
        group = 0           
        while group < len(self.n_units):
            if self.n_units[group] == 0:
                if group < self.n_defenders:
                    self.n_defenders -= 1
                del self.n_units[group]
                del self.hp[group]
                del self.ap[group]
                del self.initiative[group]
                del self.weakness[group]
                del self.immune[group]
                del self.attack_type[group]
                del self.ep[group]
                del self.target[group]
                del self.targeted[group]
                del self.group_ids[group]
                del self.possible_targets[group]
                del self.kills[group]
            else:
                group += 1
        
        for group in range(len(self.n_units)):
            self.target[group] = None
            self.targeted[group] = False


    def get_damage(self,attacker,target):

        immune = (self.attack_type[attacker] in self.immune[target]) 
        weak = (self.attack_type[attacker] in self.weakness[target]) 
        return int(not immune)*self.ep[attacker]*(1+int(weak))



    def find_target(self,group):
        if group >= self.n_defenders:
            lims = [0,self.n_defenders]
        else:
            lims = [self.n_defenders,len(self.hp)]
        
        possible_damage = [0 for hp in range(lims[0],lims[1])]
        possible_targets = []
        for target in range(lims[1]-lims[0]):
            possible_damage[target] = self.get_damage(group,target+lims[0])
            if (self.targeted[target+lims[0]] == False) and (possible_damage[target] > 0):
                possible_targets.append(target+lims[0])
        
        self.possible_targets[group] = possible_targets.copy()  

        desireable_order = np.lexsort((self.initiative[lims[0]:lims[1]],self.ep[lims[0]:lims[1]],possible_damage))[::-1]
        for target in desireable_order:
            if (self.targeted[target+lims[0]] == False) and (possible_damage[target] > 0):
                self.targeted[target+lims[0]] = True
                self.target[group] = target + lims[0]
                return

    def battle(self,verbose=False):
        n_attackers = 1
        while (self.n_defenders < len(self.n_units)) and (self.n_defenders > 0) and (n_attackers > 0):
        
            if verbose:
                print("Immune System:")
                for group in range(self.n_defenders):
                    
                    if self.n_units[group] != 1:
                        plural = "s" 
                    else: 
                        plural = ""
                    
                    print(f"Group {self.group_ids[group]} contain {self.n_units[group]} unit{plural}")
                print("Infection:")
                for group in range(self.n_defenders,len(self.n_units)):

                    if self.n_units[group] != 1:
                        plural = "s" 
                    else: 
                        plural = ""

                    print(f"Group {self.group_ids[group]} contain {self.n_units[group]} unit{plural}")  
                print()   

            self.target_selection()

            if verbose:
                for group in range(self.n_defenders,len(self.n_units)):
                    for target in self.possible_targets[group]:
                        print(f"Infection group {self.group_ids[group]} would deal defending group {self.group_ids[target]} {self.get_damage(group,target)} damage")
                for group in range(self.n_defenders):
                    for target in self.possible_targets[group]:
                        print(f"Immune system group {self.group_ids[group]} would deal defending group {self.group_ids[target]} {self.get_damage(group,target)} damage")
                print()
                
            attackers = self.attack()
            n_attackers = len(attackers)

            if verbose:
                for group in attackers:
                    if group < self.n_defenders:
                        army = "Immune System"
                    else:
                        army = "Infection"
                    if self.kills[group] != 1:
                        plural = "s" 
                    else: 
                        plural = ""

                    print(f"{army} group {self.group_ids[group]} attacks defending group {self.group_ids[self.target[group]]}, killing {self.kills[group]} unit{plural}")
                print()

            self.cleanup()
        if n_attackers == 0:
            self.winner = "Stalemate"
        else:
            if self.n_defenders > 0:
                self.winner = "Immune system"
            else:
                self.winner = "Infection"

def main(): 
    data = data_folder.joinpath("input.txt").read_text()
    
    d = Disease(data)
    d.battle()
    print("Part 1")
    print(f"The {d.winner} army wins with {sum(d.n_units)} units left")
    print()

    print("Part 2")

    upper = 1024
    lower = 0
    d = Disease(data,upper)
    d.battle()
    while d.winner in ["Infection","Stalemate"]:
        lower = upper
        upper = 2*upper 
        d = Disease(data,upper)
        d.battle()
    units_left = sum(d.n_units)

    while upper-lower > 1:
        middle = (upper+lower)//2
        
        d = Disease(data,middle)
        if middle == 31:
            d.battle(verbose=True)
        else:
            d.battle()
        if d.winner in ["Infection","Stalemate"]:
            lower = middle
        else:
            upper = middle
            units_left = sum(d.n_units)
            
    print(f"With a boost of {upper} the Immune System army wins with {units_left} units left")


if __name__ == "__main__":
    main()
