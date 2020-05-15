from pathlib import Path
from copy import deepcopy

class lights():

    def __init__(self,data):
        self.lights = [list(line) for line in data.split("\n")]    
        self.dim = [len(self.lights),len(self.lights[0])]
    def _adj_lights(self,y,x):
        adj_coords = [[y-1,x-1],
                      [y-1,x],
                      [y-1,x+1],
                      [y,x-1],
                      [y,x+1],
                      [y+1,x-1],
                      [y+1,x],
                      [y+1,x+1]]
        adj_lights = []
        for coord in adj_coords:
            if (0<= coord[0] < self.dim[0]) and (0<= coord[1] < self.dim[1]):
                adj_lights.append(self.lights[coord[0]][coord[1]])
        
        return adj_lights

    def step(self,corners_on):
        new_lights = deepcopy(self.lights)
        for y in range(self.dim[0]):
            for x in range(self.dim[1]):
                new_lights[y][x] = self._find_light_type(y,x,corners_on)
        self.lights = new_lights

    def evolve(self,t,corners_on=False, output=False):
        if corners_on:
            self.lights[0][0] = "#"
            self.lights[0][self.dim[1]-1] = "#"
            self.lights[self.dim[0]-1][0] = "#"
            self.lights[self.dim[0]-1][self.dim[1]-1] = "#"
        if output:
            print("Initial state:")
            self.print_lights()
            print()
        for i in range(t):
            self.step(corners_on)
            if output:
                print(f"After {i+1} step{'s' if i > 0 else ''}:")
                self.print_lights()
                print()

    def _find_light_type(self,y,x,corners_on):
        y_corner = (y==0) or (y==self.dim[0]-1)
        x_corner = (x==0) or (x==self.dim[1]-1)
        if corners_on and (y_corner and x_corner):
            return '#' 

        adj_lights = self._adj_lights(y,x)
        light_count = 0
        for adj_light in adj_lights:
            light_count += int(adj_light=='#')

        if self.lights[y][x] == '.':
            if light_count == 3:
                return '#'
            else:
                return '.'
        elif self.lights[y][x] == '#':
            if 2 <= light_count <= 3:
                return '#'
            else:
                return '.'
        else:
            raise RuntimeError

    def print_lights(self,ret=False):
        line = []
        for y in range(self.dim[0]):
            s = ""
            for k in self.lights[y]:
                s += k   
            line.append(s)
        output = '\n'.join(line)
        if ret:
            return output
        else:
            print(output)

    def count_lights(self):
        lights_on = 0
        for y in range(len(self.lights)):
            for x in range(len(self.lights[0])):
                if self.lights[y][x] == '#':
                    lights_on += 1
        return lights_on
def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    
    print("Part 1:")
    l = lights(data)
    t = 100
    l.evolve(t)
    print(f"After {t} steps {l.count_lights()} lights are on")
    print()
    print("Part 2:")
    l = lights(data)
    l.evolve(t,corners_on=True)
    print(f"After {t} steps {l.count_lights()} lights are on")
if __name__ == "__main__":
    main()