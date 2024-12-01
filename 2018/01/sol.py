from pathlib import Path


def main():
    data_folder = Path(__file__).parent.resolve()
    file = data_folder / "input.txt"
    freq_changes = [int(freq_change) for freq_change in file.read_text().split("\n")]
    print("Part 1")
    print(f"The sum of frequency changes are {sum(freq_changes)}")
    print("Part 2")
    unique_freq_changes = [0]
    duplicate_found = False
    current_total = unique_freq_changes[-1]
    while not duplicate_found:
        for freq_change in freq_changes:
            current_total += freq_change
            if current_total in unique_freq_changes:
                print(f"The first repeated frequency reached is {current_total}")
                duplicate_found = True
                break
            else:
                unique_freq_changes.append(current_total)

        print(len(unique_freq_changes))


if __name__ == "__main__":
    main()
