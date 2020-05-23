from pathlib import Path
import re
data_folder = Path(".").resolve()

reg = re.compile("\d+")
def main():
    data = data_folder.joinpath("input.txt").read_text()
    sheet = []
    for line in data.split("\n"):
        sheet.append([int(d) for d in reg.findall(line)])

    print("Part 1")
    checksum = 0
    for row in sheet:
        checksum += max(row)-min(row)    

    print(f"The checksum is {checksum}")
    print()

    print("Part 2")
    checksum = 0
    for row in sheet:
        found = False
        i = 0
        while not found:
            for j in range(i+1,len(row)):
                num = max(row[i],row[j])
                den = min(row[i],row[j])
                if num % den == 0:
                    checksum += num//den
                    found = True
                    break
            if i == len(row):
                raise RuntimeError("No match found for a row in the sheet")
            i += 1
    print(f"The checksum is {checksum}")

if __name__ == "__main__":
    main()
