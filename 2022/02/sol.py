from pathlib import Path

data_folder = Path(".").resolve()

symb_to_num = {"A": 1, "B": 2, "C": 3, "X": 1, "Y": 2, "Z": 3}

def parse_data(data):
    games = [[symb_to_num[symb] for symb in game.split()] for game in data.split("\n")]
    return games

def score(game,new_interpretation):
    if new_interpretation:
        offset = (game[1]-2) % 3
        played = (((game[0] - 1) + offset) % 3) + 1
        score = played + 3*(game[1]-1)
    else:
        win_factor = (1+(game[1] - game[0]) % 3) % 3
        score = game[1] + 3 * win_factor

    return score

def main():
    data = data_folder.joinpath("input.txt").read_text()
    games = parse_data(data)

    print("Part 1")
    scores = [score(game,False) for game in games]
    print(f"The total score is {sum(scores)}")
    print()

    print("Part 2")
    scores = [score(game,True) for game in games]
    print(f"The total score is {sum(scores)}")
    print()


if __name__ == "__main__":
    main()
