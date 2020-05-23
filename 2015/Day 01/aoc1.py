from pathlib import Path

data_folder = Path(".").resolve()

def find_floor(instrs):
    floor_delta = {'(':1,')':-1}
    floor = 0
    for char in instrs:
        floor += floor_delta[char]
    return floor

def find_basement_pos(instrs):
    floor_delta = {'(':1,')':-1}
    floor = 0
    for pos,char in enumerate(instrs):
        floor += floor_delta[char]
        if floor < 0:
            return pos+1
    return None

def main():
    data = data_folder.joinpath("input.txt").read_text()
    print("Part 1")
    print(f"The instructions take Santa to floor {find_floor(data)}")
    print()

    print("Part 2")
    print(f"Instruction {find_basement_pos(data)} causes Santa to first enter the basement")


if __name__ == "__main__":
    main()
