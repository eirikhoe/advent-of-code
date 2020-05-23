from pathlib import Path
import numpy as np

data_folder = Path(".").resolve()


def rep_code(data,modified=False):
    message = []
    for line in data.split("\n"):
        message.append([ord(c) for c in line])
    message = np.array(message,dtype=int)
    
    corrected_message = ""
    for col in np.arange(message.shape[1]):
        chars,counts = np.unique(message[:,col], return_counts=True)
        if modified:
            index = np.argsort(counts)[0]
        else:
            index = np.argsort(counts)[-1]
        corrected_message += chr(chars[index])
    
    return corrected_message


def main():
    data = data_folder.joinpath("input.txt").read_text()
    
    print("Part 1")
    print(f"The decoded message is {rep_code(data)}")
    print()

    print("Part 2")
    print(f"The modified decoded message is {rep_code(data,True)}")

    
if __name__ == "__main__":
    main()