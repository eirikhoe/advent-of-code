from pathlib import Path
import numpy as np
from collections import deque
import re

data_folder = Path(".").resolve()
reg = re.compile(r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+\d+T\s+\d+%")


def man_dist(pos1, pos2):
    pos1 = np.array(pos1)
    pos2 = np.array(pos2)
    return np.sum(np.abs(pos1 - pos2))


class Storage:
    def __init__(self, data):
        y = []
        x = []
        capacity_list = []
        used_list = []
        for line in data.split("\n"):
            m = reg.match(line)
            if m is not None:
                x.append(int(m.group(1)))
                y.append(int(m.group(2)))
                capacity_list.append(int(m.group(3)))
                used_list.append(int(m.group(4)))
        self.y_size = max(y) + 1
        self.x_size = max(x) + 1
        self.capacity = np.zeros((self.y_size, self.x_size), dtype=np.int16)
        self.used = np.zeros((self.y_size, self.x_size), dtype=np.int16)
        self.data_pos = (0,self.x_size-1)

        for i in range(len(x)):
            self.capacity[y[i], x[i]] = capacity_list[i]
            self.used[y[i], x[i]] = used_list[i]

    def count_viable_pairs(self):
        n_pairs = 0
        for y in np.arange(self.capacity.shape[0]):
            for x in np.arange(self.capacity.shape[1]):
                if self.used[y, x] > 0:
                    n_pairs += np.sum(self.capacity - self.used >= self.used[y, x])
                    n_pairs -= int(
                        self.capacity[y, x] - self.used[y, x] >= self.used[y, x]
                    )

        return n_pairs

    def move(self, used, candidate):
        used = np.copy(used)
        used[candidate[1]] += used[candidate[0]]
        used[candidate[0]] = 0
        return used

    def _get_candidates(self, pos):
        (y, x) = pos
        viable = []
        min_node_capacity = np.min(self.capacity)
        for candidate in [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]:
            if (
                (0 <= candidate[0] < self.y_size)
                and (0 <= candidate[1] < self.x_size)
                and (self.used[candidate] <= min_node_capacity)
                and (candidate != self.data_pos)
            ):
                viable.append(candidate)
        return viable

    def bfs(self, start, end):
        if start == end:
            return 0
        distance = np.full(self.used.shape, -1, dtype=int)
        distance[start] = 0
        queue = deque([start])
        while len(queue) > 0:
            point = queue.popleft()
            for candidate in self._get_candidates(point):
                if distance[candidate] < 0:
                    distance[candidate] = distance[point] + 1
                    if candidate == end:
                        return distance[end]
                    queue.append(candidate)
        return None

    def shortest_path(self):
        # Verify assumptions

        # There is only one free node
        assert np.sum(self.used == 0) == 1

        min_node_capacity = np.min(self.capacity)
        large_nodes = self.used > min_node_capacity
        small_nodes = np.logical_not(large_nodes)

        # The next two assertions imply large nodes are essentially walls

        # Small nodes can't take the data from large nodes
        assert np.min(self.used[large_nodes]) > np.max(self.capacity[small_nodes])

        # Large nodes can't take any additional data
        two_smallest_used = np.sort(self.used[self.used > 0])[:2]
        assert (
            np.max(self.capacity[large_nodes] - self.used[large_nodes])
            < two_smallest_used[0]
        )

        # Data can only be moved to the current free node
        assert np.sum(two_smallest_used) > np.max(self.capacity[small_nodes])

        # Implies a state is entirely defined by the position of the target data and the position
        # of the free node.

        zero_node = np.nonzero(self.used == 0)
        zero_node = list(zip(*zero_node))[0]
        state = ((0, self.x_size - 1), zero_node)
        distance = dict()
        distance[state] = 0
        queue = deque([state])
        end_point = (0, 0)
        min_distance = np.inf
        while len(queue) > 0:
            state = queue.popleft()
            curr_distance = distance[state]
            self.data_pos = state[0]
            
            for candidate in self._get_candidates(state[0]):
                new_state = (candidate, state[0])
                new_distance = curr_distance + self.bfs(state[1], candidate) + 1
                if (
                    (new_state not in distance) or (distance[new_state] > new_distance)
                ) and (new_distance < min_distance):
                    distance[new_state] = new_distance
                    if candidate == end_point:
                        min_distance = new_distance
                        continue
                    else:
                        queue.append(new_state)
                else:
                    continue
        
        return min_distance


def main():
    data = data_folder.joinpath("input.txt").read_text()
    s = Storage(data)
    print("Part 1")
    print(f"There are {s.count_viable_pairs()} viable pairs of nodes")
    print()

    print("Part 2")
    print(f"The fewest number of steps to move the goal data is {s.shortest_path()}")


if __name__ == "__main__":
    main()
