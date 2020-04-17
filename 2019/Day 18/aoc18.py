from pathlib import Path
import numpy as np
import copy
import time
data_folder = Path(__file__).parent.resolve()


class Maze:
    """A Maze class"""

    def __init__(self, map_file):
        map = [[ord(d) for d in list(x)] for x in map_file.read_text().split("\n")]
        self.map = np.array(map, dtype=int)
        self.initial_pos = self.get_initial_pos()
        self.keys, self.keys_loc = self.get_keys()
        self.key_groups = self.find_key_groupings()
        self.dist = self.compute_distance_matrix()
        self.keys_ancestors, self.doors_ancestors = self.find_ancestors()
        self.attempts = [dict()] * len(self.keys)

    def get_initial_pos(self):
        init = []
        for y in np.arange(self.map.shape[0]):
            for x in np.arange(self.map.shape[1]):
                if self.map[y, x] == ord("@"):
                    init.append((y, x))
        return init

    def bfs(self, pos):
        distance = np.full(self.map.shape, -1, dtype=int)
        distance[pos] = 0
        queue = [pos]
        while len(queue) > 0:
            point = queue.pop(0)
            for candidate in [
                (point[0], point[1] + 1),
                (point[0], point[1] - 1),
                (point[0] + 1, point[1]),
                (point[0] - 1, point[1]),
            ]:
                if (distance[candidate] < 0) and self.map[candidate] != ord("#"):
                    queue.append(candidate)
                    distance[candidate] = distance[point] + 1
        return distance

    def find_key_groupings(self):
        visited = np.full(self.map.shape, False, dtype=bool)

        keys_seen = dict()
        for i, pos in enumerate(self.initial_pos):
            count = 0
            queue = [pos]
            while len(queue) > 0:
                point = queue.pop(0)
                for candidate in [
                    (point[0], point[1] + 1),
                    (point[0], point[1] - 1),
                    (point[0] + 1, point[1]),
                    (point[0] - 1, point[1]),
                ]:
                    if not visited[candidate] and self.map[candidate] != ord("#"):
                        queue.append(candidate)
                        visited[candidate] = True

                        if ord("a") <= self.map[candidate] <= ord("z"):
                            keys_seen[self.map[candidate]] = (i, count)
                            count += 1
        return keys_seen

    def find_ancestors(self):
        visited = np.full(self.map.shape, False, dtype=bool)
        keys_seen = {pos: [] for pos in self.initial_pos}
        doors_seen = {pos: [] for pos in self.initial_pos}

        keys_ancestors = [[]] * len(self.keys)
        doors_ancestors = [[]] * len(self.keys)
        queue = self.initial_pos.copy()
        while len(queue) > 0:
            point = queue.pop(0)
            for candidate in [
                (point[0], point[1] + 1),
                (point[0], point[1] - 1),
                (point[0] + 1, point[1]),
                (point[0] - 1, point[1]),
            ]:
                if not visited[candidate] and self.map[candidate] != ord("#"):
                    queue.append(candidate)
                    visited[candidate] = True

                    keys_seen[candidate] = keys_seen[point]
                    doors_seen[candidate] = doors_seen[point]

                    if ord("a") <= self.map[candidate] <= ord("z"):
                        temp = keys_seen[candidate].copy()
                        keys_ancestors[self.map[candidate] - ord("a")] = temp.copy()
                        temp.append(self.map[candidate])
                        keys_seen[candidate] = temp
                        doors_ancestors[self.map[candidate] - ord("a")] = doors_seen[
                            candidate
                        ].copy()

                    if ord("A") <= self.map[candidate] <= ord("Z"):
                        temp = doors_seen[candidate].copy()
                        temp.append(self.map[candidate])
                        doors_seen[candidate] = temp
        return (keys_ancestors, doors_ancestors)

    def get_keys(self):
        keys_loc = dict()
        keys = []
        for y in np.arange(self.map.shape[0]):
            for x in np.arange(self.map.shape[1]):
                if ord("a") <= self.map[y, x] <= ord("z"):
                    keys.append(self.map[y, x])
                    keys_loc[self.map[y, x]] = (y, x)

        return np.array(sorted(keys), dtype=int), keys_loc

    def compute_distance_matrix(self):
        distance_matrices = []
        start_index = ord("a")
        n_keys = [0] * len(self.initial_pos)
        key_lists = []
        for i in range(len(self.initial_pos)):
            key_lists.append([])
        for key in self.key_groups:
            i = self.key_groups[key][0]
            n_keys[i] += 1
            key_lists[i].append(key)
        for i, pos in enumerate(self.initial_pos):
            distance_matrix = np.full((n_keys[i] + 1, n_keys[i]), -1, dtype=int)
            distance_start = self.bfs(pos)
            keys = key_lists[i]
            for j, label in enumerate(keys):
                distance_matrix[-1, j] = distance_start[self.keys_loc[label]]
                distance = self.bfs(self.keys_loc[label])
                for k, label_other in enumerate(keys):
                    distance_matrix[j, k] = distance[self.keys_loc[label_other]]
            distance_matrices.append(distance_matrix)
        return distance_matrices

    def solve(
        self,
        current_symbols=None,
        robot_id=0,
        collected=None,
        dist=0,
        min_dist=[int(1e7)],
    ):
        if collected is None:
            collected = np.full(len(self.keys), False, dtype=bool)
        if current_symbols is None:
            current_symbols = [ord("@")] * len(self.key_groups)
        key = (tuple(collected), tuple(current_symbols))
        attempt_index = np.sum(collected, dtype=int) - 1
        if key in self.attempts[attempt_index]:
            if self.attempts[attempt_index][key] <= dist:
                return
        self.attempts[attempt_index][key] = dist

        if collected.all():
            if dist < min_dist[0]:
                min_dist[0] = dist
            return
        else:
            dist_best_estimate = dist
            for key in self.keys[~collected]:
                group_id, index = self.key_groups[key]
                dist_best_estimate += np.min(self.dist[group_id][:, index], axis=0)
            if dist_best_estimate >= min_dist[0]:
                return

        for switch in self.find_candidates(collected):
            robot_id_new, j = self.key_groups[switch]
            if current_symbols[robot_id_new] == ord("@"):
                distance_row = -1
            else:
                temp, distance_row = self.key_groups[current_symbols[robot_id_new]]
            dist_new = dist + self.dist[robot_id_new][distance_row, j]
            collected_new = np.copy(collected)
            collected_new[switch - ord("a")] = True
            level = np.sum(collected_new)
            current_symbols_new = current_symbols.copy()
            current_symbols_new[robot_id_new] = switch
            self.solve(
                current_symbols_new, robot_id_new, collected_new, dist_new, min_dist
            )

        if sum([symbol == ord("@") for symbol in current_symbols]) == len(
            self.key_groups
        ):
            return min_dist[0]

    def find_candidates(self, collected):
        candidates = []
        for i, doors in enumerate(self.doors_ancestors):
            if not collected[i]:
                can_reach = True
                for door in doors:
                    if not collected[door - ord("A")]:
                        can_reach = False
                        break
                for key in self.keys_ancestors[i]:
                    if not collected[key - ord("a")]:
                        can_reach = False
                        break
                if can_reach and not collected[i]:
                    candidates.append(i + ord("a"))
        return candidates


def main():
    start_time = time.perf_counter()
    print('Part 1')
    file = data_folder / "day_18_1_input.txt"
    maze = Maze(file)
    print(f"It takes {maze.solve()} steps to collect all the keys")
    print()

    print('Part 2')
    file = data_folder / "day_18_2_input.txt"
    maze = Maze(file)
    print(f"It takes {maze.solve()} steps to collect all the keys")

    print(time.perf_counter() - start_time)
if __name__ == "__main__":
    main()
