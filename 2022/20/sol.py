from pathlib import Path
from copy import deepcopy
data_folder = Path(".").resolve()

def parse_data(data):
    values = [int(d) for d in data.split("\n")]
    n = len(values)
    file = [((i-1)%n,(i+1)%n,v) for i,v in enumerate(values)]
    for i,value in enumerate(values):
        if value == 0:
            break

    return file,i

def get_relative_element(file,index,n):
    m = len(file)-1
    n = n % m
    if n == 0:
        return index
    for _ in range(n):
        index = file[index][1]
    return index


def move(file,index):
    el = file[index]
    if el[2] == 0:
        return file
    prev = get_relative_element(file,index,el[2])
    next = file[prev][1]
    file[index] = (prev,next,el[2])
    file[el[0]] = (file[el[0]][0],el[1],file[el[0]][2])
    file[el[1]] = (el[0],file[el[1]][1],file[el[1]][2])
    file[prev] = (file[prev][0],index,file[prev][2])
    file[next] = (index,file[next][1],file[next][2])
    return file

def get_relative_value(file,index,n):
    n = n % len(file)
    for _ in range(n):
        index = file[index][1]
    return file[index][2]

def get_array_from_index(file,initial_index):
    array = []
    for i,_ in enumerate(file):
        array.append(get_relative_value(file,initial_index,i))
    return array

def get_groove_coordinate_sum(file,zero_index):
    groove_coordinates = [get_relative_value(file,zero_index,i) for i in [1000,2000,3000]]
    return sum(groove_coordinates)


def mix(file):
    for i,_ in enumerate(file): 
        file = move(file,i)
    return file

def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    file,zero_index = parse_data(data)



    print("Part 1")
    mixed_file = deepcopy(file)
    mixed_file = mix(mixed_file)
    groove_coordinate_sum = get_groove_coordinate_sum(mixed_file,zero_index)
    print(f"The groove coordinate sum is {groove_coordinate_sum}.")
    print()

    print("Part 2")
    key = 811589153
    mixed_file = [(el[0],el[1],el[2]*key) for el in file]
    for _ in range(10):
        mixed_file = mix(mixed_file)
    groove_coordinate_sum = get_groove_coordinate_sum(mixed_file,zero_index)
    print(f"The actual groove coordinate sum is {groove_coordinate_sum}.")
    print()


if __name__ == "__main__":
    main()
