from pathlib import Path
import re
from collections import deque
data_folder = Path(".").resolve()

def reduce(moves):
    curr_len = len(moves)
    old_len = curr_len+1
    step_counts = {'ne':0,'se':0,'nw':0,'sw':0,'s':0,'n':0}
    for i,move in enumerate(moves):
        step_counts[move] += 1

    canc_pairs = [['ne','sw'],['n','s'],['nw','se']]
    abbrevs = [['ne','nw','n'],
               ['se','sw','s'],
               ['nw','s','sw'],
               ['ne','s','se'],
               ['sw','n','nw'],
               ['se','n','ne']]


    while old_len > curr_len:
        old_len = curr_len
        for pair in canc_pairs:
            if step_counts[pair[0]] and step_counts[pair[1]]:
                red_amount = min(step_counts[pair[0]],step_counts[pair[1]])
                step_counts[pair[0]] -= red_amount
                step_counts[pair[1]] -= red_amount

        for abbrev in abbrevs:
            if step_counts[abbrev[0]] and step_counts[abbrev[1]]:
                red_amount = min(step_counts[abbrev[0]],step_counts[abbrev[1]])
                step_counts[abbrev[0]] -= red_amount
                step_counts[abbrev[1]] -= red_amount
                step_counts[abbrev[2]] += red_amount

        curr_len = 0
        for direction in step_counts:
            curr_len += step_counts[direction] 
    return curr_len


def main():
    data = data_folder.joinpath("input.txt").read_text()
    moves = [d for d in data.split(',')]     
    n_moves = reduce(moves)
    print("Part 1")
    print(f"The fewest number of steps required to reach the child is {n_moves}")
    print()

    print("Part 2")
    max_distance = n_moves
    
    i = n_moves+1
    while i <= len(moves):
        n_moves = reduce(moves[:i])
        if n_moves > max_distance:
            max_distance = n_moves
            i += 1
        else:
            i += (max_distance-n_moves+1)
    print(f"The longest away the child ever got was {max_distance} steps")

if __name__ == "__main__":
    main()
