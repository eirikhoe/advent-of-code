from pathlib import Path
import numpy as np

data_folder = Path(".")


class IntCodeProgram:
    """A Class for the state of an IntCode program"""

    def __init__(self, instr):
        self.instructions = dict(zip(list(range(len(instrs))), instrs))
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


class Robot:
    """A class for a hull painting robot"""
    
    def __init__(self, prog, initial_panel_color=0):
        self.location = (0, 0)
        self.panel_colors = {(0, 0): initial_panel_color}
        self.times_painted = {(0, 0): 0}
        self.orientation = 0
        self.prog = IntCodeProgram(prog)

    def paint_panel(self, color_int):
        self.panel_colors[self.location] = color_int
        self.times_painted[self.location] += 1

    def move(self, right):
        if right:
            self.orientation = (self.orientation + 90) % 360
        else:
            self.orientation = (self.orientation - 90) % 360

        if self.orientation == 0:
            self.location = (self.location[0] - 1, self.location[1])
        elif self.orientation == 90:
            self.location = (self.location[0], self.location[1] + 1)
        elif self.orientation == 180:
            self.location = (self.location[0] + 1, self.location[1])
        elif self.orientation == 270:
            self.location = (self.location[0], self.location[1] - 1)

        if self.location not in self.panel_colors:
            self.panel_colors[self.location] = 0
            self.times_painted[self.location] = 0

    def get_n_tiles_painted(self):
        tiles_painted = 0
        for tile in self.times_painted:
            if self.times_painted[tile] > 0:
                tiles_painted += 1
        return tiles_painted

    def print_hull(self):
        row_dim = [0, 0]
        column_dim = [0, 0]
        tile_rows = []
        tile_columns = []
        colors = []
        for tile in self.panel_colors:
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
            colors.append(self.panel_colors[tile])

        tile_rows = np.array(tile_rows)
        tile_columns = np.array(tile_columns)
        hull = np.zeros(
            (row_dim[1] - row_dim[0] + 1, column_dim[1] - column_dim[0] + 1), dtype=int
        )
        hull[tile_rows - row_dim[0], tile_columns - column_dim[0]] = colors
        
        # Assumes text color is white on the system
        print(
            "\n".join(
                [
                    "".join([str(d) for d in row])
                    .replace("0", " ")
                    .replace("1", u"\u2588")
                    for row in hull
                ]
            )
        )


def add(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    prog.set(
        prog.instr_ptr + 2,
        modes[2],
        prog.get(prog.instr_ptr, modes[0]) + prog.get(prog.instr_ptr + 1, modes[1]),
    )
    prog.instr_ptr += n_params
    return None


def mult(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    prog.set(
        prog.instr_ptr + 2,
        modes[2],
        prog.get(prog.instr_ptr, modes[0]) * prog.get(prog.instr_ptr + 1, modes[1]),
    )
    prog.instr_ptr += n_params


def inp(prog, modes):
    n_params = 1
    modes = modes + [0] * (n_params - len(modes))
    prog.set(prog.instr_ptr, modes[0], prog.input)
    prog.instr_ptr += n_params


def outp(prog, modes):
    n_params = 1
    modes = modes + [0] * (n_params - len(modes))
    prog.output = prog.get(prog.instr_ptr, modes[0])
    prog.instr_ptr += n_params


def jump_if_true(prog, modes):
    n_params = 2
    modes = modes + [0] * (n_params - len(modes))

    if prog.get(prog.instr_ptr, modes[0]) > 0:
        prog.instr_ptr = prog.get(prog.instr_ptr + 1, modes[1])
    else:
        prog.instr_ptr += n_params


def jump_if_false(prog, modes):
    n_params = 2
    modes = modes + [0] * (n_params - len(modes))

    if prog.get(prog.instr_ptr, modes[0]) == 0:
        prog.instr_ptr = prog.get(prog.instr_ptr + 1, modes[1])
    else:
        prog.instr_ptr += n_params


def less_than(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    if prog.get(prog.instr_ptr, modes[0]) < prog.get(prog.instr_ptr + 1, modes[1]):
        prog.set(prog.instr_ptr + 2, modes[2], 1)
    else:
        prog.set(prog.instr_ptr + 2, modes[2], 0)
    prog.instr_ptr += n_params


def equals(prog, modes):
    n_params = 3
    modes = modes + [0] * (n_params - len(modes))
    if prog.get(prog.instr_ptr, modes[0]) == prog.get(prog.instr_ptr + 1, modes[1]):
        prog.set(prog.instr_ptr + 2, modes[2], 1)
    else:
        prog.set(prog.instr_ptr + 2, modes[2], 0)
    prog.instr_ptr += n_params


def adj_rel_base(prog, modes):
    n_params = 1
    modes = modes + [0] * (n_params - len(modes))
    prog.rel_base += prog.get(prog.instr_ptr, modes[0])
    prog.instr_ptr += n_params


operations = {
    1: add,
    2: mult,
    3: inp,
    4: outp,
    5: jump_if_true,
    6: jump_if_false,
    7: less_than,
    8: equals,
    9: adj_rel_base,
}


def run_robot(robot):
    end_of_program = False
    output_type = "color"
    while not end_of_program:
        digits = [int(d) for d in str(robot.prog.get(robot.prog.instr_ptr, 1))]
        if len(digits) == 1:
            op_mode = digits[-1]
        else:
            op_mode = digits[-2] * 10 + digits[-1]
        if op_mode == 99:
            return
        else:
            modes = digits[-3::-1]
            robot.prog.instr_ptr += 1
            if op_mode == 3:
                robot.prog.input = robot.panel_colors[robot.location]
            operations[op_mode](robot.prog, modes)

            if op_mode == 4:
                if output_type == "color":
                    robot.paint_panel(robot.prog.output)
                    output_type = "direction"
                elif output_type == "direction":
                    robot.move(robot.prog.output)
                    output_type = "color"


file = data_folder / "day_11_input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]

def main(): 
    # Part 1
    robot = Robot(instrs, 0)
    run_robot(robot)
    print("Part 1:")
    print(f"{robot.get_n_tiles_painted()} tiles were painted at least once.")
    print()

    # Part 2
    robot = Robot(instrs, 1)
    run_robot(robot)
    print("Part 2:")
    print(f"The completed hull looks like:")
    robot.print_hull()

if __name__ == "__main__":
    main()
