from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    grid = [list(line) for line in data.split("\n")]
    return grid


def count_word_occurences(string, word):
    index = -1
    count = -1
    while (index != -1) or (count == -1):
        index = string.find(word, index + 1)
        count += 1
    return count


def count_word_and_backwards(string, word):
    count = count_word_occurences(string, word)
    count += count_word_occurences(string, word[::-1])
    return count


def count_xmas(grid):
    word = "XMAS"
    n_rows = len(grid)
    n_cols = len(grid[0])
    count = 0
    for i in range(n_rows):
        string = "".join(grid[i])
        count += count_word_and_backwards(string, word)

    for i in range(n_cols):
        string = "".join([row[i] for row in grid])
        count += count_word_and_backwards(string, word)

    start_inds = [(i, 0) for i in range(n_rows)]
    start_inds += [(0, j) for j in range(1, n_cols)]
    for start_ind in start_inds:
        string = ""
        i, j = start_ind
        while (j < n_cols) and (i < n_rows):
            string += grid[i][j]
            i += 1
            j += 1
        count += count_word_and_backwards(string, word)

    start_inds = [(i, n_cols - 1) for i in range(n_rows)]
    start_inds += [(0, j) for j in range(n_cols - 1)]
    for start_ind in start_inds:
        string = ""
        i, j = start_ind
        while (j >= 0) and (i < n_rows):
            string += grid[i][j]
            i += 1
            j -= 1
        count += count_word_and_backwards(string, word)

    return count

def count_x_mas(grid):
    n_rows = len(grid)
    n_cols = len(grid[0])
    count = 0
    for i in range(n_rows-2):
        for j in range(n_cols-2):
            part = [row[j:j+3] for row in grid[i:i+3]]
            count += find_x_mas(part)
    return count

def find_x_mas(grid):
    pos_diag = "".join([grid[i][i] for i in range(3)])
    neg_diag = "".join([grid[i][2-i] for i in range(3)])
    word = "SAM"
    count = 0
    for diag in [pos_diag,neg_diag]:
        if (diag != word) and (diag != word[::-1]):
            break
    else:
        count = 1
    return count

    

       





def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    grid = parse_data(data)

    print("Part 1")
    print(f"The word XMAS was found {count_xmas(grid)} times.")
    print()

    print("Part 2")
    print(f"There were {count_x_mas(grid)} X-MAS occurences.") 
    print()


if __name__ == "__main__":
    main()
