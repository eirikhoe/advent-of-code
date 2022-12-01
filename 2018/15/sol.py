from pathlib import Path
import numpy as np
import copy
import time
from colorama import init
data_folder = Path(__file__).parent.resolve()
init()
class Troop:
    def __init__(self,pos,race,attack=3):
        self.attack = attack
        self.race = race
        self.hp = 200
        self.pos = pos

def _get_candidates(point):
    return [
                (point[0] - 1, point[1]),
                (point[0], point[1] - 1),
                (point[0], point[1] + 1),
                (point[0] + 1, point[1]),
            ]

class Battle:
    """A Battle class"""

    def __init__(self, map_file,attack=3):
        map = [[d for d in x] for x in map_file.read_text().split("\n")]
        self.map = map
        self.map_size = (len(map),len(map[0]))
        self.troops = self.get_initial_troops(attack)
        self.round = 0
        self.killed = {'E':0,'G':0}
    
    def get_initial_troops(self,attack):
        troops = []
        for y in range(self.map_size[0]):
            for x in range(self.map_size[1]):
                if self.map[y][x] == 'E':
                    troops.append(Troop((y,x),'E',attack))
                elif self.map[y][x] == 'G':
                    troops.append(Troop((y,x),'G'))

        return troops

    def _pos_value(self,pos):
        return pos[0]*self.map_size[1]+pos[1]

    def troop_order(self):
        troop_pos_values = [self._pos_value(t.pos) for t in self.troops]
        return list(np.argsort(troop_pos_values))

    def bfs(self, pos):
        distance = np.full(self.map_size, -1, dtype=int)
        distance[pos] = 0
        queue = [pos]
        while len(queue) > 0:
            point = queue.pop(0)
            for candidate in _get_candidates(point):
                if (distance[candidate] < 0) and (self.map[candidate[0]][candidate[1]] != "#"):
                    distance[candidate] = distance[point] + 1
                    if self.map[candidate[0]][candidate[1]] == ".":
                        queue.append(candidate)
        return distance

    def turn(self):

        order = self.troop_order()
        k = 0
        while k < len(order):
            k_increase = 1
            i = order[k]
            attack = False
            distance = self.bfs(self.troops[i].pos)
            enemy_index = []
            enemy_distances = []
            for j in range(len(self.troops)):
                if self.troops[j].race != self.troops[i].race:
                    enemy_index.append(j)
                    enemy_distance = distance[self.troops[j].pos]
                    if enemy_distance in [1,2]:
                        attack = True
                    enemy_distances.append(enemy_distance)
            
            if not enemy_index:
                return True

            if (1 not in enemy_distances) and (max(enemy_distances) > 0): 
                open_squares = []
                for j in enemy_index:
                    for pos in _get_candidates(self.troops[j].pos):
                        if (self.map[pos[0]][pos[1]] == ".") and (pos not in open_squares):
                            open_squares.append(pos)
                
                min_dist = int(1e9)
                for pos in open_squares:
                    if 0 < distance[pos] <= min_dist:
                        if distance[pos] < min_dist:
                            dest = pos
                            min_dist = distance[pos]
                        elif self._pos_value(pos) < self._pos_value(dest):
                            dest = pos
                
                distance_from_dest = self.bfs(dest)
                for candidate in _get_candidates(self.troops[i].pos):
                    if (distance_from_dest[candidate] == min_dist-1) and (self.map[candidate[0]][candidate[1]] == "."):
                        new_pos = candidate
                        break
                pos = self.troops[i].pos 
                self.troops[i].pos = new_pos
                self.map[pos[0]][pos[1]] = "."
                self.map[new_pos[0]][new_pos[1]] = self.troops[i].race

            self.print_map()
            if attack:
                possible_targets = []
                for candidate in _get_candidates(self.troops[i].pos):
                    content = self.map[candidate[0]][candidate[1]]
                    if (content in ['G','E']) and (content != self.troops[i].race):
                        possible_targets.append(candidate)

                min_hp = None
                
                for target in possible_targets:
                    for j,troop in enumerate(self.troops):
                        if troop.pos == target:
                            break
                    if (min_hp is None) or (troop.hp < min_hp):
                        target_ind = j
                        min_hp = troop.hp
                self.troops[target_ind].hp -= self.troops[i].attack

                if self.troops[target_ind].hp <= 0:
                    self.killed[self.troops[target_ind].race] += 1
                    pos = self.troops[target_ind].pos
                    self.map[pos[0]][pos[1]] = "."
                    del self.troops[target_ind]
                    
                    for m in range(len(order)):
                        if order[m] > target_ind:
                            order[m] -= 1
                        elif order[m] == target_ind:
                            target_ord = m
                    
                    del order[target_ord]
                    if target_ord < k:
                        k_increase = 0
            
            self.print_map()
            time.sleep(0.01)

            k += k_increase
        return False

    def sim_battle(self):
        finished = False
        self.print_map()
        while not finished:

            finished = self.turn()
            if finished:
                self.print_map()
                break
            self.round += 1
        total_hp_left = sum([troop.hp for troop in self.troops])
        winner_dict = {'E':'Elves','G':'Goblins'}
        print(f"Combat ends after {self.round} full rounds")
        print(f"{winner_dict[self.troops[0].race]} win with {total_hp_left} total hit points left")
        print(f"Outcome: {self.round} * {total_hp_left} = {self.round*total_hp_left}")
        print(f"{self.killed['E']} elves and {self.killed['G']} goblins died.")
    def print_map(self):
        order = self.troop_order()
        s = [f"\033[2;1HAfter {self.round} rounds:"]
        for y,row in enumerate(self.map):
            r = "".join(row)
            r += "   "
            troops_on_row = []
            for ind in order:
                troop = self.troops[ind]
                if troop.pos[0] == y:
                    troops_on_row.append(f"{troop.race}({troop.hp})")
            r += ", ".join(troops_on_row)
            r += " "*(80-len(r))
            s.append(r)
        print("\n".join(s))


def main():
    file = data_folder / "input.txt"
    battle = Battle(file)
    battle.sim_battle()
    battle = Battle(file,34)
    battle.sim_battle()

if __name__ == "__main__":
    main()
