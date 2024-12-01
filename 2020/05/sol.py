from pathlib import Path


def compute_seat_id(seat):
    seat_id = ""
    for c in seat[:7]:
        seat_id += str(int(c == "B"))
    for c in seat[7:]:
        seat_id += str(int(c == "R"))
    seat_id = int(seat_id, 2)

    return seat_id


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    seats = data.split("\n")

    print("Part 1")
    seat_ids = []
    for seat in seats:
        seat_id = compute_seat_id(seat)
        seat_ids.append(seat_id)
    seat_ids.sort()
    print(f"The highest seat ID on a boarding pass is {seat_ids[-1]}")
    print()

    print("Part 2")
    for i, _ in enumerate(seat_ids[:-1]):
        if seat_ids[i + 1] - seat_ids[i] == 2:
            print(f"Your seat has seat ID {seat_ids[i]+1}")
            break


if __name__ == "__main__":
    main()
