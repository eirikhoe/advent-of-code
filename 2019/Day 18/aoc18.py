from pathlib import Path
import numpy as np
import copy
import time
from colorama import init
from math import ceil,floor

init()
data_folder = Path(__file__).parent.resolve()
start_time = time.perf_counter()

def bfs(maze,start):
    distance = np.full(maze.shape,-1,dtype=int)
    distance[start] = 0
    queue= [start]
    while len(queue) > 0:
        point = queue.pop(0)
        for candidate in [(point[0],point[1]+1),(point[0],point[1]-1),(point[0]+1,point[1]),(point[0]-1,point[1])]:
            if (distance[candidate] < 0) and maze[candidate] != ord('#'):
                queue.append(candidate)
                distance[candidate] = distance[point]+1
    return distance
        
    


def main():
    file = data_folder / "day_18_input.txt"
    
    asteroids = [
    [ord(d) for d in list(x)]
    for x in file.read_text().split("\n")
    ]
    asteroids = np.array(asteroids, dtype=int)
    distance = bfs(asteroids,(1,15))
    print(distance)
if __name__ == "__main__":
    main()
