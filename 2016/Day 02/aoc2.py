from pathlib import Path

data_folder = Path(".").resolve()

def find_code(instrs,keypad=None):
    moves = {'D':(1,0),'U':(-1,0),'L':(0,-1),'R':(0,1)}
    code = ""
    
    if keypad is None:
        keypad = []
        for i in range(3):
            keypad.append([])
            for j in range(3):
                keypad[-1].append(str(1+3*i+j))

    for i,row in enumerate(keypad):
        for j,button in enumerate(row):
            if button == "5":
                pos = (i,j)
    
    for line in instrs:
        for instr in list(line):
            new_pos = (pos[0]+moves[instr][0],pos[1]+moves[instr][1])
            if (0 <= new_pos[0] < len(keypad)) and (0 <= new_pos[1] < len(keypad[0])):
                if keypad[new_pos[0]][new_pos[1]] != " ":
                    pos = new_pos
        code += keypad[pos[0]][pos[1]]
    return code

def main():
    data = data_folder.joinpath("input.txt").read_text()
    instructions = data.split("\n")
    
    print("Part 1")
    print(f"The bathroom code is {find_code(instructions)}")
    print()
    
    print("Part 2")
    keypad = ["  1  "," 234 ","56789"," ABC ","  D  "]
    keypad = [list(row) for row in keypad]
    print(f"The bathroom code is {find_code(instructions,keypad)}")


if __name__ == "__main__":
    main()
