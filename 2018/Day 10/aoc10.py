from pathlib import Path
import numpy as np
import re
from collections import defaultdict
import re
from collections import deque

def main():
    data_folder = Path(".").resolve()
    text = data_folder.joinpath("input.txt").read_text().split("\n")
    reg = re.compile(r"position=< *(-?\d+), *(-?\d+)> velocity=< *(-?\d+), *(-?\d+)>")
    data = []
    for line in text:
        data.append([int(d) for d in reg.match(line).group(1,2,3,4)])
    
    sky = Sky(data)
    time = sky.find_time_to_look()
    print(f"After {time} seconds the following message appears")
    sky.print_sky(time)


class Sky():

    def __init__(self,lights):
        self.x_init = np.array([light[0] for light in lights],dtype=int)
        self.y_init = np.array([light[1] for light in lights],dtype=int)
        self.vx = np.array([light[2] for light in lights],dtype=int)
        self.vy = np.array([light[3] for light in lights],dtype=int)

    def _get_row_col_lim(self,x,y):
        row_dim = [np.min(y), np.max(y)]
        column_dim = [np.min(x), np.max(x)]

        return row_dim, column_dim

    def advance(self,t):
        x = self.x_init + t*self.vx
        y = self.y_init + t*self.vy
        return x,y

    def find_time_to_look(self):
        row_dim, col_dim = self._get_row_col_lim(self.x_init,self.y_init)
        old_area = np.diff(row_dim).astype(float)*np.diff(col_dim).astype(float)  
        min_found = False
        i = 0
        while not min_found:
            i += 1
            x,y = self.advance(i)
            row_dim, col_dim = self._get_row_col_lim(x,y)
            area = np.diff(row_dim).astype(float)*np.diff(col_dim).astype(float)  
            if area > old_area:
                min_found = True
            old_area = area
        return i-1

    def print_sky(self,t):
        
        x,y = self.advance(t)
        row_dim, column_dim = self._get_row_col_lim(x,y)

        map_array = np.full(
            (row_dim[1] - row_dim[0] + 1, column_dim[1] - column_dim[0] + 1),0,dtype=int
        )
        map_array[y - row_dim[0], x - column_dim[0]] = 1
        print(
            "\n".join(
                [
                    "".join([str(d) for d in row])
                    .replace("0", ".")
                    .replace("1", "#")
                    for row in map_array
                ]
            )
        )



if __name__ == "__main__":
    main()