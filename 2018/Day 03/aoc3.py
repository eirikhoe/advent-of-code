from pathlib import Path
import numpy as np
import re

def main():
    data_folder = Path(".").resolve()
    find_coords = re.compile(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)")
    data = data_folder.joinpath("input.txt").read_text()
    claims = np.array(
        [[int(d) for d in position] for position in find_coords.findall(data)]
    )
    min_x = np.min(claims[:,1])
    claims[:,[1,3]] -= min_x
    size_x = np.max(claims[:,1]+claims[:,3])
    
    min_y = np.min(claims[:,2])
    claims[:,[2,4]] -= min_y
    size_y = np.max(claims[:,2]+claims[:,4])

    fabric = np.zeros((size_y,size_x),dtype=int)

    for claim_nr in np.arange(claims.shape[0]):
        fabric[claims[claim_nr,2]:claims[claim_nr,2]+claims[claim_nr,4],claims[claim_nr,1]:claims[claim_nr,1]+claims[claim_nr,3]] += 1
    print("Part 1:")
    print(f"The total square inches of overlapping claims are: {np.sum(fabric > 1)}")

    print("Part 2")    
    for claim_nr in np.arange(claims.shape[0]):
        if np.sum(fabric[claims[claim_nr,2]:claims[claim_nr,2]+claims[claim_nr,4],claims[claim_nr,1]:claims[claim_nr,1]+claims[claim_nr,3]] > 1) == 0:
            print(f"Claim #{claims[claim_nr,0]} does not overlap any other claim") 


    

if __name__ == "__main__":
    main()