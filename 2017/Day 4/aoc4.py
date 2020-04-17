from pathlib import Path
import re
data_folder = Path(".").resolve()

def valid_passphrase(passphrase):
    return len(set(passphrase)) == len(passphrase)

def valid_passphrase_anagram(passphrase):
    for j in range(len(passphrase)):
        passphrase[j] = "".join(sorted(list(passphrase[j])))
    
    return len(set(passphrase)) == len(passphrase)

def main():
    data = data_folder.joinpath("input.txt").read_text()
    passphrases = []
    for line in data.split("\n"):
        passphrases.append(line.split(" "))
    
    print("Part 1")
    n_valid = 0
    for passphrase in passphrases:
        n_valid += int(valid_passphrase(passphrase))


    print(f"{n_valid} passphrases are valid")
    print()

    print("Part 2")
    n_valid = 0
    for passphrase in passphrases:
        n_valid += int(valid_passphrase_anagram(passphrase))

    print(f"{n_valid} passphrases are valid")

if __name__ == "__main__":
    main()
