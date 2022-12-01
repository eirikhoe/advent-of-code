from pathlib import Path


def transformation(value, subject_number):
    return (value * subject_number) % 20201227


def find_loop_size(public_key):
    subject_number = 7
    value = 1
    loop_size = 0
    while value != public_key:
        value = transformation(value, subject_number)
        loop_size += 1
    return loop_size


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    card_public_key, door_public_key = (int(d) for d in data.split("\n"))
    card_loop_size = find_loop_size(card_public_key)
    encryption_key = 1
    for i in range(card_loop_size):
        encryption_key = transformation(encryption_key, door_public_key)

    print("Part 1")
    print(f"The encryption key that the door and key is trying ")
    print(f"to establish is {encryption_key}")
    print()


if __name__ == "__main__":
    main()
