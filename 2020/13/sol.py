from pathlib import Path
from math import gcd, prod


def find_earliest_bus(min_depart_time, bus_ids):
    valid_buses = [int(id) for id in bus_ids if id != "x"]
    print(prod(valid_buses))
    depart_time = min_depart_time
    while True:
        for bus_id in valid_buses:
            if depart_time % bus_id == 0:
                wait_time = depart_time - min_depart_time
                return wait_time, bus_id
        depart_time += 1


def find_first_streak(bus_ids):
    buses = [(int(id), n) for n, id in enumerate(bus_ids) if id != "x"]

    start_time = 0
    bus_id = 0
    skip_size = 1
    while bus_id < len(buses):
        bus = buses[bus_id]
        while (start_time + bus[1]) % bus[0] != 0:
            start_time += skip_size
        skip_size = (skip_size * bus[0]) // gcd(skip_size, bus[0])
        bus_id += 1
    return start_time


def main():
    data_folder = Path(__file__).parent.resolve()
    data = data_folder.joinpath("input.txt").read_text()
    data = data.split("\n")
    min_depart_time = int(data[0])
    bus_ids = data[1].split(",")

    print("Part 1")
    wait_time, bus_id = find_earliest_bus(min_depart_time, bus_ids)
    bus_prod = wait_time * bus_id
    print("The ID of the earliest bus you can take to the airport multiplied by ")
    print(f"the number of minutes you'll need to wait for that bus is {bus_prod}")
    print()

    print("Part 2")
    streak_start = find_first_streak(bus_ids)
    print("The earliest timestamp such that all of the listed bus IDs depart at ")
    print(f"offsets matching their positions in the list is {streak_start}")


if __name__ == "__main__":
    main()
