from pathlib import Path

data_folder = Path(".").resolve()

def find_two_factors(entries,total):
    for i,entry in enumerate(entries):
        if total-entry in entries[i+1:]:
            return entry, total-entry
    return None

def find_three_factors(entries,total):
    for i,entry in enumerate(entries[:-1]):
        last_two = find_two_factors(entries[i+1:],total-entry)
        if last_two:
            return entry, last_two[0], last_two[1]
    return None

def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = [int(d) for d in data.split("\n")]
    total = 2020
    first, second = find_two_factors(data,total)
    print("Part 1")
    print(f"The product of the two entries that sum to {total} is {first*second}")
    print()

    first, second, third = find_three_factors(data,total)
    print("Part 2")
    print(f"The product of the three entries that sum to {total} is {first*second*third}")
    print()

if __name__ == "__main__":
    main()
