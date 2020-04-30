from pathlib import Path
import numpy as np
from collections import deque
import re

data_folder = Path(".").resolve()
reg = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+\d+T\s+\d+%")

def man_dist(pos1,pos2):
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    return np.sum(np.abs(pos1-pos2))


class Storage:

    def __init__(self,data):
        y = []
        x = []
        capacity_list = []
        used_list = []
        for line in data.split('\n'):
            m = reg.match(line)
            if m is not None:
                x.append(int(m.group(1)))
                y.append(int(m.group(2)))
                capacity_list.append(int(m.group(3)))
                used_list.append(int(m.group(4)))
        self.y_size = max(y)+1
        self.x_size = max(x)+1
        self.capacity = np.zeros((self.y_size,self.x_size),dtype=np.int16)
        self.used = np.zeros((self.y_size,self.x_size),dtype=np.int16)
        
        for i in range(len(x)):
            self.capacity[y[i],x[i]] = capacity_list[i]
            self.used[y[i],x[i]] = used_list[i]

    
    def count_viable_pairs(self):
        n_pairs = 0
        for y in np.arange(self.capacity.shape[0]):
            for x in np.arange(self.capacity.shape[1]):
                if self.used[y,x] > 0:
                    n_pairs += np.sum(self.capacity-self.used >= self.used[y,x])
                    n_pairs -= int(self.capacity[y,x]-self.used[y,x] >= self.used[y,x])
            
        return n_pairs
    

    def move(self,used,candidate):
        used = np.copy(used)
        used[candidate[1]] += used[candidate[0]]
        used[candidate[0]] = 0
        return used
        
    
    
    def adjacent_viable_pairs(self,used,pos):
        (y,x) = pos
        viable = []
        if used[pos] > 0:
            for adj_pos in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
                if ((0 <= adj_pos[0] < self.y_size) 
                    and (0 <= adj_pos[1] < self.x_size)  
                    and (self.capacity[adj_pos]-used[adj_pos] >= used[pos])
                    ):
                    viable.append([pos,adj_pos]) 
        return viable

    def reverse_viable_pairs(self,used,adj_pos,last_to):
        (y,x) = adj_pos
        viable = []
        for pos in [(y-1,x),(y+1,x),(y,x-1),(y,x+1)]:
            if ((0 <= pos[0] < self.y_size) 
                and (0 <= pos[1] < self.x_size)  
                and (self.capacity[adj_pos]-used[adj_pos] >= used[pos])
                and (used[pos] > 0)    
                and (pos != last_to)
                ):
                    viable.append([pos,adj_pos]) 
        return viable

    def all_adjacent_viable_pairs(self,used):
        viable = []
        for y in range(self.y_size):
            for x in range(self.x_size):
                pos = (y,x)
                viable += self.adjacent_viable_pairs(used,pos)
        return viable

    def get_yx(self,i):
        y = i // self.x_size
        x = i % self.x_size
        return (y,x)
    
    def get_index(self,pos):
        index = pos[0]*self.x_size + pos[1]
        return index

    def shortest_path_new(self):
        # Verify assumptions

        # There is only one free node
        assert np.sum(self.used==0) == 1

        min_node_capacity = np.min(self.capacity)
        large_nodes = (self.used > min_node_capacity)
        
        large_indicies = np.nonzero(large_nodes)
        print(self.used[large_indicies])

    def shortest_path(self):
        state = (self.x_size-1,(),())
        seen_states = np.copy(self.used).reshape(1,self.y_size,self.x_size)
        seen_data_pos = np.array([self.x_size-1],dtype=np.int16)
        queue = deque([state])
        max_distance = 0
        while len(queue) > 0:
            state = queue.popleft()
            used = np.copy(self.used)
            distance = len(state[1])
            data_pos = self.get_yx(state[0])
            if distance == 0:
                candidates = self.all_adjacent_viable_pairs(used)
            else:
                # print('State:')
                for i in range(distance):
                    pos_from = self.get_yx(state[1][i])
                    pos_to = self.get_yx(state[2][i])
                    used = self.move(used,[pos_from,pos_to])
                last_pos = self.get_yx(state[1][distance-1])
                last_to = self.get_yx(state[2][distance-1])
                if last_to != data_pos:
                    candidates = self.reverse_viable_pairs(used,last_pos,last_to)
                else:
                    candidates = self.all_adjacent_viable_pairs(used)
                    for candidate in candidates:
                        if (candidate[0] == last_to) and (candidate[1] == last_pos):
                            candidates.remove(candidate)
                            break
                # print(used)
                # print(data_pos)
                # print(distance)
                # print(candidates)
                # print()
                # input()
            for candidate in candidates:
                new_used = self.move(used,candidate)
                new_data_pos = data_pos
                if candidate[0] == data_pos:
                    new_data_pos = candidate[1]
                new_state_from = list(state[1])
                new_state_from.append(self.get_index(candidate[0]))
                new_state_to = list(state[2])
                new_state_to.append(self.get_index(candidate[1]))
                data_ind = self.get_index(new_data_pos)
                new_state = (data_ind,tuple(new_state_from),tuple(new_state_to))

                
                seen_before = False
                for i,s in enumerate(seen_data_pos):
                    if data_ind == s:
                        if np.array_equal(new_used,seen_states[i]):
                            seen_before = True
                            break

                if seen_before:
                    continue
                else:
                    queue.append(new_state)
                    seen_states = np.append(seen_states,new_used.reshape(1,self.y_size,self.x_size))
                    seen_data_pos = np.append(seen_data_pos,np.array([data_ind],dtype=np.int16))
                    if new_data_pos == (0,0):
                        return distance + 1
                    if distance >= max_distance:
                        max_distance = distance +1
                        print(max_distance,len(queue))
        
        # for key in distance:
        #     print(key[0])
        #     used = np.array(key[1],dtype=int)
        #     used = used.reshape((self.y_size,self.x_size))
        #     for y in range(self.y_size):
        #         print(" ".join([str(d) for d in used[y]]))
        #     print(distance[key])
        #     print()
        return None
def main():
    data = data_folder.joinpath("input.txt").read_text()
    s = Storage(data)
    print("Part 1")
    print(f"There are {s.count_viable_pairs()} viable pairs of nodes")
    print()
    print(s.shortest_path_new())

if __name__ == "__main__":
    main()
