from pathlib import Path
import numpy as np

data_folder = Path(".").resolve()


def parse_data(data):
    lines = data.split("\n")
    drawn_numbers = [int(d) for d in lines[0].split(",")]
    boards = []
    board = []
    for line in lines[2:]:
        if (not line) and board:
            boards.append(board)
            board = []
        else:
            board.append([int(d) for d in line.split()])
    if board:
        boards.append(board)
    boards = np.array(boards, dtype=int)
    return drawn_numbers, boards


def compute_board_score(drawn_numbers, boards, win):
    picked = np.full_like(boards, fill_value=False, dtype=bool)
    is_bingo = np.full(boards.shape[0], fill_value=False, dtype=bool)
    desired_ind = None
    for number in drawn_numbers:
        prior_is_bingo = is_bingo
        picked[boards == number] = True
        best_col = np.max(np.sum(picked, axis=1), axis=1)
        best_row = np.max(np.sum(picked, axis=2), axis=1)
        is_bingo = np.maximum(best_row, best_col) == boards.shape[2]
        if win and np.any(is_bingo):
            desired_ind = np.arange(boards.shape[0])[is_bingo][0]
            break
        elif (not win) and np.all(is_bingo):
            desired_ind = np.arange(boards.shape[0])[np.logical_not(prior_is_bingo)][0]
            break

    if desired_ind is not None:
        bingo_board = boards[desired_ind]
        picked_on_board = picked[desired_ind]
        sum_unpicked = np.sum(bingo_board[np.logical_not(picked_on_board)])
        return sum_unpicked * number


def main():
    data = data_folder.joinpath("input.txt").read_text()
    drawn_numbers, boards = parse_data(data)

    print("Part 1")
    score = compute_board_score(drawn_numbers, boards, win=True)
    print(f"The score if we choose the board winning first will be {score}")
    print()

    print("Part 2")
    score = compute_board_score(drawn_numbers, boards, win=False)
    print(f"The score if we choose the board winning last will be {score}")
    print()


if __name__ == "__main__":
    main()
