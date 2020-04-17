from pathlib import Path
import re

class Bridge:
    
    def __init__(self,data):

        self.components = []
        for line in data.split("\n"):
            self.components.append([int(connector) for connector in line.split('/')])
        self.longest_ind = []
        self.longest_strength = -1

    def strength(self,indexes):
        strength = 0
        for index in indexes:
            strength += sum(self.components[index])
        return strength

    def find_strongest(self):
        return self._long_strong_step(0,[])

    def _long_strong_step(self,end_connector,used):

        strongest_bridge = -1
        for i,component in enumerate(self.components):
            if i not in used:
                for j,connector in enumerate(component):
                    if connector == end_connector:
                        curr_used = used.copy()
                        curr_used.append(i)
                        bridge = sum(component) + self._long_strong_step(component[1-j],curr_used)
                        if bridge > strongest_bridge: 
                            strongest_bridge = bridge
                            new_used = curr_used
                        break    

        if strongest_bridge >= 0:
            strong_long = self.strength(new_used)
            if ((len(new_used) > len(self.longest_ind))
                or ((len(new_used) == len(self.longest_ind)) and (strong_long > self.longest_strength))
            ):
                self.longest_strength = strong_long
                self.longest_ind = new_used
            return strongest_bridge
        else:
            return 0
        

def main(): 
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    b = Bridge(data)
    print(f"The strongest bridge has a strength of {b.find_strongest()}")
    print()

    print("Part 2")
    print(f"The longest strongest bridge has a strength of {b.longest_strength}")

if __name__ == "__main__":
    main()
