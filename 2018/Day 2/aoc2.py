from pathlib import Path
import numpy as np

def main(): 
    data_folder = Path(__file__).parent.resolve()
    file = data_folder / "input.txt"
    ids = [np.array(list(id)) for id in file.read_text().split("\n")]
    count_twos = 0
    count_threes = 0
    for id in ids:
        temp,count = np.unique(id,return_counts=True)
        if 2 in count:
            count_twos += 1
        if 3 in count:
            count_threes += 1
    
    print(f"The checksum is: {count_twos*count_threes}.")
    n_ids = len(ids)
    for i in np.arange(n_ids):
        for j in np.arange(i+1,n_ids):
            if ids[i].size == ids[j].size:
                differing_chars = 0
                for k in np.arange(ids[i].size):
                    if ids[i][k] != ids[j][k]:
                        differing_chars += 1
                        differing_pos = k
                if differing_chars == 1:
                    index = np.full(ids[i].shape,True)
                    index[differing_pos] = False
                    print(f"The common box ID letters are {''.join(list(ids[i][index]))}")
                


if __name__ == "__main__":
    main()
