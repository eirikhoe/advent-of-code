from pathlib import Path
import numpy as np
import copy
import time
import os
from colorama import init
init()
data_folder = Path(__file__).parent.resolve()

rg = np.random.default_rng()

class IntCodeProgram:
    """A Class for the state of an IntCode program"""

    def __init__(self, instr):
        self.instructions = dict(zip(list(range(len(instrs))), instrs))
        self._init_instructions = copy.deepcopy(self.instructions)
        self.rel_base = 0
        self.instr_ptr = 0
        self.input = None
        self.output = None

    def get(self, ptr, mode):
        loc = self._find_loc(ptr, mode)
        if loc in self.instructions:
            return self.instructions[loc]
        else:
            return 0

    def set(self, ptr, mode, value):
        loc = self._find_loc(ptr, mode)
        self.instructions[loc] = value

    def _find_loc(self, ptr, mode):
        if mode == 1:
            return ptr
        elif mode == 0:
            return self.get(ptr, 1)
        elif mode == 2:
            return self.get(ptr, 1) + self.rel_base
    
    def reset(self):
        self.rel_base = 0
        self.instr_ptr = 0
        self.input = None
        self.output = None
        self.instructions = copy.deepcopy(self._init_instructions)

    def add(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        self.set(
            self.instr_ptr + 2,
            modes[2],
            self.get(self.instr_ptr, modes[0]) + self.get(self.instr_ptr + 1, modes[1]),
        )
        self.instr_ptr += n_params
        return None


    def mult(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        self.set(
            self.instr_ptr + 2,
            modes[2],
            self.get(self.instr_ptr, modes[0]) * self.get(self.instr_ptr + 1, modes[1]),
        )
        self.instr_ptr += n_params


    def inp(self, modes):
        n_params = 1
        modes = modes + [0] * (n_params - len(modes))
        self.set(self.instr_ptr, modes[0], self.input)
        self.instr_ptr += n_params


    def outp(self, modes):
        n_params = 1
        modes = modes + [0] * (n_params - len(modes))
        self.output = self.get(self.instr_ptr, modes[0])
        self.instr_ptr += n_params


    def jump_if_true(self, modes):
        n_params = 2
        modes = modes + [0] * (n_params - len(modes))

        if self.get(self.instr_ptr, modes[0]) > 0:
            self.instr_ptr = self.get(self.instr_ptr + 1, modes[1])
        else:
            self.instr_ptr += n_params


    def jump_if_false(self, modes):
        n_params = 2
        modes = modes + [0] * (n_params - len(modes))

        if self.get(self.instr_ptr, modes[0]) == 0:
            self.instr_ptr = self.get(self.instr_ptr + 1, modes[1])
        else:
            self.instr_ptr += n_params


    def less_than(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        if self.get(self.instr_ptr, modes[0]) < self.get(self.instr_ptr + 1, modes[1]):
            self.set(self.instr_ptr + 2, modes[2], 1)
        else:
            self.set(self.instr_ptr + 2, modes[2], 0)
        self.instr_ptr += n_params


    def equals(self, modes):
        n_params = 3
        modes = modes + [0] * (n_params - len(modes))
        if self.get(self.instr_ptr, modes[0]) == self.get(self.instr_ptr + 1, modes[1]):
            self.set(self.instr_ptr + 2, modes[2], 1)
        else:
            self.set(self.instr_ptr + 2, modes[2], 0)
        self.instr_ptr += n_params


    def adj_rel_base(self, modes):
        n_params = 1
        modes = modes + [0] * (n_params - len(modes))
        self.rel_base += self.get(self.instr_ptr, modes[0])
        self.instr_ptr += n_params

    operations = {
        1: add,
        2: mult,
        3: inp,
        4: outp,
        5: jump_if_true,
        6: jump_if_false,
        7: less_than,
        8: equals,
        9: adj_rel_base
    }

    def operate(self,op_code,modes):
        op = IntCodeProgram.operations[op_code]
        return op(self,modes)



class Droid:
    """A class for an Droid"""
    map = {(0,0):1}
    distance = {(0,0):0}
    max_distance = 0
    oxygen_system_location = None

    def __init__(self, prog):
        self.prog = IntCodeProgram(prog)
        self.location = (0,0)
        self.last_move_dir = 1

    @classmethod
    def reset_map_at_oxygen_system(cls):
        cls.map = {cls.oxygen_system_location:2}
        cls.distance = {cls.oxygen_system_location:0}
        cls.max_distance = 0
    
    def update_map(self,dir,status):

        new_location = self.new_location(dir)
        if new_location not in Droid.map:
            Droid.map[new_location] = status
            if status == 2:
                Droid.oxygen_system_location = new_location


    def update_distance(self):
        if self.location not in Droid.distance:     
            possible_distances = []
            for dir in range(1,5):
                loc = self.new_location(dir)
                if (loc in Droid.distance) and (Droid.map[loc] != 0):
                    possible_distances.append(Droid.distance[loc])
            Droid.distance[self.location] = min(possible_distances)+1
            if Droid.distance[self.location] > Droid.max_distance:
                Droid.max_distance = Droid.distance[self.location]
        # Check for cycle
        for dir in range(1,5):
            loc = self.new_location(dir)
            if (loc in Droid.distance) and (np.abs(Droid.distance[loc]-Droid.distance[self.location]) != 1):
                raise RuntimeError('Cycle found')


    def new_location(self,dir):
        if dir == 1:
            return (self.location[0] - 1, self.location[1])
        elif dir == 4:
            return (self.location[0], self.location[1] + 1)
        elif dir == 2:
            return (self.location[0] + 1, self.location[1])
        elif dir == 3:
            return (self.location[0], self.location[1] - 1)

    def rotate(self,dir,deg):
        dirs = np.array([1,4,2,3])
        dir_index = np.array([0,2,3,1])
        deg_index = np.array(deg)//90
        index = (dir_index[dir-1] + deg_index) % 4
        return dirs[index]
    
    def move(self, dir, status):
        if status != 0:
            self.location = self.new_location(dir)

    def print_map(self):
        row_dim = [0, 0]
        column_dim = [0, 0]
        tile_rows = []
        tile_columns = []
        types = []
        for tile in Droid.map:
            if tile[0] > row_dim[1]:
                row_dim[1] = tile[0]
            elif tile[0] < row_dim[0]:
                row_dim[0] = tile[0]
            if tile[1] > column_dim[1]:
                column_dim[1] = tile[1]
            elif tile[1] < column_dim[0]:
                column_dim[0] = tile[1]
            tile_rows.append(tile[0])
            tile_columns.append(tile[1])
            types.append(self.map[tile])

        tile_rows = np.array(tile_rows)
        tile_columns = np.array(tile_columns)
        map_array = np.full(
            (row_dim[1] - row_dim[0] + 1, column_dim[1] - column_dim[0] + 1),4,dtype=int
        )
        map_array[tile_rows - row_dim[0], tile_columns - column_dim[0]] = types
        map_array[self.location[0]-row_dim[0],self.location[1]-column_dim[0]] = 3
        map_array[0-row_dim[0],0-column_dim[0]] = 5
        print(f"\033[2;1HDistance: {str(Droid.distance[self.location]).rjust(3,'0')}\t\t Max distance: {str(Droid.max_distance).rjust(3,'0')}")
        print(
            "\n".join(
                [
                    "".join([str(d) for d in row])
                    .replace("0", u"\u2588")
                    .replace("1", ".")
                    .replace("2", u"\u2605")
                    .replace("3","D")
                    .replace("4"," ")
                    .replace("5","S")
                    for row in map_array
                ]
            )
        )
        
    def find_move_dir(self):
        surroundings = np.zeros(4,dtype=int)
        for i,possible_direction in enumerate(self.rotate(self.last_move_dir,[0,90,180,270])):
            if self.new_location(possible_direction) not in Droid.map:
                return possible_direction
                
            else:
                surroundings[i] = Droid.map[self.new_location(possible_direction)]
        
        rotation = None
        if sum(surroundings == 0) == 3:
            rotation = np.array([0,90,180,270])[surroundings != 0]
        elif sum(surroundings == 0) == 2:
            rotations = np.array([0,90,180,270])[surroundings != 0]
            rotation = rotations[rotations != 180][0]
        elif surroundings[1] != 0:
            rotation = 90
        elif surroundings[0] != 0:
            rotation = 0

        if rotation is not None:           
            return self.rotate(self.last_move_dir,rotation)

        return 1
                

    def run(self,exit_on_found_oxygen=True):
        os.system('cls' if os.name == 'nt' else 'clear')
        end_of_program = False
        self.prog.input = 1
        
        while not end_of_program:
            digits = [int(d) for d in str(self.prog.get(self.prog.instr_ptr, 1))]
            if len(digits) == 1:
                op_mode = digits[-1]
            else:
                op_mode = digits[-2] * 10 + digits[-1]
            if op_mode == 99:
                end_of_program = True
            else:
                modes = digits[-3::-1]
                self.prog.instr_ptr += 1
                if op_mode == 3:
                    self.prog.input = self.find_move_dir()
                self.prog.operate(op_mode,modes)
                if op_mode == 4:
                    self.update_map(self.prog.input,self.prog.output)
                    self.move(self.prog.input,self.prog.output)
                    self.update_distance()

                    self.print_map()
                    if self.prog.output != 0:
                        self.last_move_dir = self.prog.input
                    if exit_on_found_oxygen and (self.prog.output == 2):
                        end_of_program = True
        self.print_map()


file = data_folder / "day_15_input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]

def main(): 
    second_part = True
    droid = Droid(instrs)
    droid.run()
    if second_part:
        Droid.reset_map_at_oxygen_system()
        droid.run(False)
if __name__ == "__main__":
    main()
