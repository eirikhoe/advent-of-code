from pathlib import Path

data_folder = Path(".").resolve()

def rotate(v,direction):

    rotated = {'L':(-v[1],v[0]),'R':(v[1],-v[0])}
    return rotated[direction]

def find_hq(instructions,stop_at_duplicate):
    
    x = 0
    y = 0
    curr_dir = (-1,0)
    if stop_at_duplicate:
        visited = {(0,0)}
        found_duplicate = False
    for instruction in instructions:
        rot_dir = instruction[0]
        distance = int(instruction[1:])
        curr_dir = rotate(curr_dir,rot_dir)
    
        if stop_at_duplicate:
            y_t = y
            x_t = x
            for d in range(1,distance):
                y_t += curr_dir[0]
                x_t += curr_dir[1]
                if (y_t,x_t) in visited:
                    found_duplicate = True
                    x = x_t
                    y = y_t
                    break
                else:
                    visited.add((y_t,x_t))
            if found_duplicate:
                break    

        y += curr_dir[0]*distance
        x += curr_dir[1]*distance
    return abs(x)+abs(y)

def main():
    data = data_folder.joinpath("input.txt").read_text()
    instructions = data.split(", ")
    
    print("Part 1")
    print(f"The Easter Bunny HQ is {find_hq(instructions,False)} blocks away")
    print()

    print("Part 2")
    print(f"The Easter Bunny HQ is {find_hq(instructions,True)} blocks away")


if __name__ == "__main__":
    main()
