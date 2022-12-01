from pathlib import Path
import numpy as np
import re
from collections import defaultdict
import re
from collections import deque
def main():
    data_folder = Path(".").resolve()
    text = data_folder.joinpath("input.txt").read_text()
    reg = re.compile(r"(\d+) players; last marble is worth (\d+) points")
    m = reg.match(text)
    n_players = int(m.group(1))
    high_value = int(m.group(2))
    high_score = sim_game(n_players,high_value)
    print(high_score)

def sim_game(n_players,high_value):
    circle = deque([0])
    scores = [0 for i in range(n_players)]
    current_player = 1
    for marble in range(1,high_value+1):
        if (marble % 23) == 0:
            scores[current_player] += marble
            circle.rotate(7)
            scores[current_player] += circle.pop()
            circle.rotate(-1)
        else: 
            circle.rotate(-1)
            circle.append(marble)
            current_player = (current_player + 1) % n_players
        if marble % int(1e5) == 0:
            print(marble)
    return max(scores)

if __name__ == "__main__":
    main()