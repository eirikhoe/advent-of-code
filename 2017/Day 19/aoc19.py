from pathlib import Path
from copy import deepcopy
from time import sleep

def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text().split("\n")
    data = [list(line) for line in data]
    p = Packet(data)
    p.move()
    print("Part 1")
    print(f"The packet will see (in order) the letters {p.letters}")
    print()

    print("Part 2")
    print(f"The packet needs to go {p.n_steps} steps")

class Packet():
    
    @classmethod
    def rot(self,v,type):
        rotated = {'R':(-v[1],v[0]),'L':(v[1],-v[0]),'S':v}
            
        return rotated[type]

    def __init__(self,data):
        data = deepcopy(data)
        self.track = data
        self.letters = ""
        self.pos = self.find_start_pos()
        self.dir = (1,0)
        self.n_steps = 1


    def find_start_pos(self):
        for i,pos in enumerate(self.track[0]):
            if pos == '|':
                return (0,i)

    def inbounds(self,pos):
        return (0 <= pos[0] < len(self.track)) and (0 <= pos[1] < len(self.track[0]))
    def move(self):
        while True:
            y,x = self.pos
            vy,vx = self.dir
            if  65 <= ord(self.track[y][x]) <= 90:
                self.letters += self.track[y][x]

            if self.inbounds((y+vy,x+vx)) and (self.track[y+vy][x+vx] != " "):
                self.pos = (y+vy,x+vx)
            else:
                alt_v = [(1-abs(vy),1-abs(vx)),(-1+abs(vy),-1+abs(vx))]
                path_end = True
                for v in alt_v:
                    if (self.inbounds((y+v[0],x+v[1]))) and (self.track[y+v[0]][x+v[1]] != ' '):
                        self.pos = (y+v[0],x+v[1])
                        self.dir = v
                        path_end = False
                if path_end:
                    break
            self.n_steps += 1

    def print_track(self):
        track = deepcopy(self.track)
        track[self.pos[0]][self.pos[1]] = '#'
        s = ""
        s += "Found letters: " + self.letters + '\n\n'
        col_size = len(track[0])
        col_digits = len(str(col_size-1))
        form_str = "{:" + str(col_digits) + "d}"
        for j in range(col_digits):
            s += " "
            for loc in range(col_size):
                loc_str = form_str.format(loc)
                s += loc_str[j]
            s += "\n"

        row_size = len(track)
        row_digits = len(str(row_size-1))
        form_str = "{:" + str(row_digits) + "d}"
        for y in range(row_size):
            s += form_str.format(y)
            s += "".join(track[y])    
            s += "\n"
        print(s)               


if __name__ == "__main__":
    main()