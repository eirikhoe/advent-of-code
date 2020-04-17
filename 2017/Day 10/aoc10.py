from pathlib import Path
import re
from collections import deque
data_folder = Path(".").resolve()

def knot_hash_round(lengths,elements,skip_size=0,index=0):
    n_elements = len(elements)
    elements = deque(elements)
    for j,length in enumerate(lengths):
        elements.rotate(-index)
        reverse = list(elements)[length-1::-1]
        for i in range(length):
            elements[i] = reverse[i]
        elements.rotate(index)
        index = (index + length + skip_size) % n_elements
        skip_size += 1
    return list(elements),skip_size,index

def knot_hash(lengths):
    index = 0
    std_lengths = [17, 31, 73, 47, 23]
    lengths += std_lengths
    skip_size = 0
    n_elements = 256
    elements = list(range(n_elements))
    for i in range(64):
        elements,skip_size,index = knot_hash_round(lengths,elements,skip_size,index)
    output = ""
    block_len = 16
    n_blocks = 256//block_len
    for i in range(n_blocks):
        init_ind = i*block_len
        value = elements[init_ind]
        for j in range(init_ind+1,(i+1)*block_len):
            value ^= elements[j]
        output += hex(value)[2:].zfill(2)
    return output

def main():
    data = data_folder.joinpath("input.txt").read_text()
    lengths = [int(d) for d in data.split(',')]     
    elements,_,_ = knot_hash_round(lengths,list(range(256)))
    print("Part 1")
    print(f"After the procedure the product of the first two elements is {elements[0]*elements[1]}")
    print()

    print("Part 2")
    data = data_folder.joinpath("input.txt").read_text()
    lengths = [ord(d) for d in data]     
    print(f"The Knot Hash of the input is {knot_hash(lengths)}")
    
if __name__ == "__main__":
    main()
