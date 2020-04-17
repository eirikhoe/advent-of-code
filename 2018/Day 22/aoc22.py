from __future__ import print_function

from pathlib import Path
import numpy as np
from collections import deque
data_folder = Path(".").resolve()


class Cave:

    def __init__(self,depth,target):
        self.mouth = (0,0)
        self.depth = depth
        self.target = (target[1],target[0])
        self.erosion = np.array([[self._erosion(0)]],dtype=np.int16)
        self.lims = (0,0)
        self.expand(self.target)

    def _gen_values(self,y,x):
        x = int(x)
        y = int(y)
        if (y,x) in [self.mouth,self.target]:
            geo_ind = 0
        elif y == 0:
            geo_ind = x*16807
        elif x==0:
            geo_ind = y*48271
        else:
            geo_ind = int(self.erosion[y-1,x]) * int(self.erosion[y,x-1])        
        self.erosion[y,x] = self._erosion(geo_ind)
    
    def _type(self,y,x):
        return self.erosion[y,x] % 3
    
    def expand(self,new_lim):
        new_columns = np.zeros((self.lims[0]+1,new_lim[1]-self.lims[1]),dtype=np.int16)

        self.erosion = np.append(self.erosion,new_columns,axis=1)
        
        new_rows = np.zeros((new_lim[0]-self.lims[0],new_lim[1]+1),dtype=np.int16)

        self.erosion = np.append(self.erosion,new_rows,axis=0)
        
        for y in range(self.lims[0]+1):
            for x in range(self.lims[1]+1,new_lim[1]+1):
                self._gen_values(y,x)            

        for y in range(self.lims[0]+1,new_lim[0]+1):
            for x in range(new_lim[1]+1):
                self._gen_values(y,x)

        self.lims = new_lim

    def find_risk_level(self,coord):
        risk_level = 0
        for y in range(coord[0]+1):
            for x in range(coord[1]+1):
                risk_level += self._type(y,x)
        return risk_level

    def _erosion(self,geo_ind):
        return (geo_ind + self.depth) % 20183

    def print_cave(self,coord):
        if (coord[0] > self.lims[0]) or (coord[1] > self.lims[1]):
            self.expand(coord)
        symb_dict = {0:".",1:"=",2:"|"}
        s = ""
        for y in range(self.lims[0]+1):
            for x in range(self.lims[1]+1):
                if (y,x) == (0,0):
                    s += "M"
                elif (y,x) == self.target:
                    s += "T"
                else:
                    cur_type = self._type(y,x)
                    s += symb_dict[cur_type]
            s += "\n"
        data_folder.joinpath("output.txt").write_text(s)    
    
    def upper_time_bound(self):
        curr_eq = 1
        x = 0
        y = 0
        time = 0
        while (y,x) != self.target:
            if (y < self.target[0]) and (self._type(y+1,x) != curr_eq):
                time +=1
                y +=1
            elif (x < self.target[1]) and (self._type(y,x+1) != curr_eq):
                time +=1
                x +=1
            elif y < self.target[0]:
                time += 8
                curr_eq = self._get_equip((y,x),(y+1,x),curr_eq)
                y +=1
            else:
                time += 8
                curr_eq = self._get_equip((y,x),(y,x+1),curr_eq)
                x +=1
        if curr_eq != 1:
            time += 7
        return time

    def _get_equip(self,point,new_point,old_eq):
        new_type = self._type(new_point[0],new_point[1])
        old_type = self._type(point[0],point[1])
        if old_eq == old_type:
            raise RuntimeError("Equipment failure")
        else:
            if (old_type == new_type):
                ans = old_eq
            else:
                eq = {0,1,2}-{old_type,new_type}
                ans = eq.pop()    
        
        
        return ans



    def _get_candidates(self,point):
        
        new_points = [
                    (point[0] - 1, point[1]),
                    (point[0], point[1] - 1),
                    (point[0], point[1] + 1),
                    (point[0] + 1, point[1]),
                ]
        return new_points 


    def shortest_route(self):
        pos = (self.mouth[0],self.mouth[1],1)
        time = dict()
        time[pos] = 0
        change_time = 7
        time_bound = self.upper_time_bound()
        queue = deque([pos])
        while len(queue) > 0:
            point = queue.popleft()
            if (point[0] >= self.lims[0]) or (point[1] >= self.lims[1]):
                self.expand((max(point[0],self.lims[0])+1,max(point[1],self.lims[1])+1))
            for candidate in self._get_candidates(point):
                if (candidate[0] < 0) or (candidate[1] < 0):
                    continue
                cand_eq = self._get_equip(point,candidate,point[2])
                candidate = (candidate[0],candidate[1],cand_eq)
                t = time[point] + 1 + 7*int(point[2] != candidate[2])
                if (candidate not in time) or (t < time[candidate]):
                    best_point_time = t+10*(self.target[0]+self.target[1])
                    for eq in range(3):
                        key = (*candidate[:2],eq)
                        if (eq != cand_eq) and (key in time):
                            best_point_time = time[key]+7

                    lim_t = (time_bound - abs(candidate[0]-self.target[0])
                             - abs(candidate[1]-self.target[1]) - 7*int(candidate[2] != 1))
                    lim_t = min(lim_t,best_point_time)
                    if t < lim_t:
                        time[candidate] = t
                        queue.append(candidate)
                        if (candidate[:2] == self.target) and ((t + 7*int(candidate[2] != 1)) < time_bound):
                            time_bound = t + 7*int(candidate[2] != 1)

        min_time = time_bound
        key = (*self.target[:2],1)
        if (key in time) and (time[key]<min_time):
            min_time = time[key]
        key = (*self.target[:2],2)
        if (key in time) and (time[key]+7<min_time):
            min_time = time[key]+7

        return min_time



def main(): 
    print("Part 1:")
    c = Cave(8103,(9,758))
    print(f"The total risk for the smallest rectangle including the target and mouth is {c.find_risk_level(c.target)}")
    c.print_cave(c.target)
    print()
    print("Part 2:")
    print(f"The shortest route to the target takes {c.shortest_route()}")

if __name__ == "__main__":
    main()
