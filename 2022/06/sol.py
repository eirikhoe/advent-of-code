from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    return data.strip()


def find_start_marker(stream, packet_len):
    n = len(stream)
    for i in range(n - packet_len + 1):
        sequence = set(stream[i : i + packet_len])
        if len(sequence) == packet_len:
            return i + packet_len


def main():
    data = data_folder.joinpath("input.txt").read_text()
    stream = parse_data(data)

    print("Part 1")
    print(f"The first marker is after character {find_start_marker(stream,4)}")
    print()

    print("Part 2")
    print(f"The first message is after character {find_start_marker(stream,14)}")
    print()


if __name__ == "__main__":
    main()
