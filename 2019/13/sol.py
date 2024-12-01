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


class Game:
    """A class for an IntCode Game"""

    def __init__(self, prog):
        self.board = {}
        self.prog = IntCodeProgram(prog)
        self.score = 0
        self.ball_loc = (0, 0)
        self.paddle_loc = (1000, 1000)

    def draw_block(self, location, block_type):
        self.board[location] = block_type
        if block_type == 4:
            self.ball_loc = location
        if block_type == 3:
            self.paddle_loc = location

    def get_n_block_tiles(self):
        n_block_tiles = 0
        for location in self.board:
            if self.board[location] == 2:
                n_block_tiles += 1
        return n_block_tiles

    def print_board(self):
        row_dim = [0, 0]
        column_dim = [0, 0]
        tile_rows = []
        tile_columns = []
        colors = []
        for tile in self.board:
            if tile[1] > row_dim[1]:
                row_dim[1] = tile[1]
            elif tile[1] < row_dim[0]:
                row_dim[0] = tile[1]
            if tile[0] > column_dim[1]:
                column_dim[1] = tile[0]
            elif tile[0] < column_dim[0]:
                column_dim[0] = tile[0]
            tile_rows.append(tile[1])
            tile_columns.append(tile[0])
            colors.append(self.board[tile])

        tile_rows = np.array(tile_rows)
        tile_columns = np.array(tile_columns)
        board = np.zeros(
            (row_dim[1] - row_dim[0] + 1, column_dim[1] - column_dim[0] + 1), dtype=int
        )
        board[tile_rows - row_dim[0], tile_columns - column_dim[0]] = colors

        print(
            f"\033[2;1HSCORE: {self.score}\t\t   BLOCKS LEFT: {self.get_n_block_tiles()}"
        )
        print(
            "\n".join(
                [
                    "".join([str(d) for d in row])
                    .replace("0", " ")
                    .replace("1", "\u2588")
                    .replace("2", "\u25a0")
                    .replace("3", "\u2500")
                    .replace("4", "\u25cf")
                    for row in board
                ]
            )
        )
        time.sleep(0.01)

    def run(self):
        os.system("cls" if os.name == "nt" else "clear")
        end_of_program = False
        output_type = ["x", "y", "type"]
        output_index = 0
        current_location = [0, 0]
        self.prog.reset()
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
                    self.prog.input = np.sign(self.ball_loc[0] - self.paddle_loc[0])
                    self.print_board()
                operations[op_mode](self.prog, modes)
                if op_mode == 4:
                    if output_type[output_index] == "x":
                        current_location[0] = self.prog.output
                    elif output_type[output_index] == "y":
                        current_location[1] = self.prog.output
                    elif output_type[output_index] == "type":
                        if (current_location[0] == -1) and (current_location[1] == 0):
                            self.score = self.prog.output
                        else:
                            self.draw_block(tuple(current_location), self.prog.output)
                    output_index = (output_index + 1) % 3
        self.print_board()


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


file = data_folder / "input.txt"
instrs = [int(instr) for instr in file.read_text().split(",")]


def main():
    # Part 1
    game = Game(instrs)
    game.run()
    initial_blocks = game.get_n_block_tiles()

    game.prog.set(0, 1, 2)
    game.run()
    if game.get_n_block_tiles() == 0:
        print(f"All {initial_blocks} blocks have been destroyed!")
        print("GAME OVER")
    else:
        print(f"Failed to destroy all {initial_blocks} blocks!")
        print("GAME OVER")


if __name__ == "__main__":
    main()
