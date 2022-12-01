from pathlib import Path
import re
from dataclasses import dataclass
from copy import deepcopy
from collections import defaultdict
from typing import DefaultDict

data_folder = Path(".").resolve()
reg = re.compile(r"Player (\d+) starting position: (\d+)")


def parse_data(data):
    players = []
    for line in data.split("\n"):
        _, pos = reg.match(line).groups()
        players.append(Player(score=0, pos=int(pos)))
    return players


@dataclass
class Player:
    score: int
    pos: int


@dataclass
class Game:
    players: list[Player]
    win_score: int
    die: int = 1
    n_die_rolls = 0
    board_size: int = 10
    winner: int = None

    def update_die(self):
        self.die = (self.die % 100) + 1
        self.n_die_rolls += 1

    def turn(self):
        for i, player in enumerate(self.players):
            for _ in range(3):
                player.pos = ((player.pos + self.die - 1) % self.board_size) + 1
                self.update_die()

            player.score += player.pos
            if player.score >= self.win_score:
                self.winner = i
                break

    def play(self):
        while self.winner is None:
            self.turn()

    def part1(self):
        return self.players[1 - self.winner].score * self.n_die_rolls


@dataclass
class Dirac_Game:
    init_pos: list[int]
    win_score: int
    games: DefaultDict = None
    won: list[int] = None
    board_size: int = 10

    def turn(self):
        for i, _ in enumerate(self.init_pos):
            new_games = defaultdict(int)
            for die, n_outcomes in zip(range(3, 10), [1, 3, 6, 7, 6, 3, 1]):
                for standing in self.games:
                    new_standing = list(standing)
                    new_standing[2 * i] = ((standing[2 * i] + die - 1) % self.board_size) + 1
                    new_standing[2 * i + 1] += new_standing[2 * i]
                    if new_standing[2 * i + 1] >= self.win_score:
                        self.won[i] += self.games[standing] * n_outcomes
                    else:
                        new_games[tuple(new_standing)] += self.games[standing] * n_outcomes
            self.games = new_games

    def play(self):
        self._setup()
        while self.games:
            self.turn()

    def _setup(self):
        self.won = [0 for _ in range(len(self.init_pos))]
        self.games = defaultdict(int)
        init_standing = []
        for i in range(len(self.init_pos)):
            init_standing.extend([self.init_pos[i], 0])
        self.games[tuple(init_standing)] = 1


def main():
    data = data_folder.joinpath("input.txt").read_text()
    players = parse_data(data)

    print("Part 1")
    game = Game(players=deepcopy(players), win_score=1000)
    game.play()
    print(f"The desired value is {game.part1()}")
    print()

    print("Part 2")
    game = Dirac_Game(init_pos=[p.pos for p in players], win_score=21)
    game.play()
    print(
        f"The player that wins in more universes with Dirac dice wins in {max(game.won)} universes"
    )
    print()


if __name__ == "__main__":
    main()
