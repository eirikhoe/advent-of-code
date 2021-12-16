from pathlib import Path
import math
from dataclasses import dataclass

data_folder = Path(".").resolve()


def parse_data(data):
    parsed = [hex2bin(c) for c in data]
    parsed = "".join(parsed)
    return parsed


def hex2bin(hex):
    return bin(int(hex, 16))[2:].zfill(4)


@dataclass
class Packet:
    version: int
    p_type: int
    data: list | int

    def compute_value(self):
        match self.p_type:
            case 0:
                return sum(subpacket.compute_value() for subpacket in self.data)
            case 1:
                return math.prod(subpacket.compute_value() for subpacket in self.data)
            case 2:
                return min(subpacket.compute_value() for subpacket in self.data)
            case 3:
                return max(subpacket.compute_value() for subpacket in self.data)
            case 4:
                return self.data
            case 5:
                return int(self.data[0].compute_value() > self.data[1].compute_value())
            case 6:
                return int(self.data[0].compute_value() < self.data[1].compute_value())
            case 7:
                return int(self.data[0].compute_value() == self.data[1].compute_value())


def parse_packet(packet):
    version = int(packet[:3], 2)
    type_id = int(packet[3:6], 2)
    if type_id == 4:
        ind, number = read_number(packet[6:])
        return ind + 6, Packet(version=version, p_type=type_id, data=number)
    subpackets = []
    if packet[6] == "0":
        subpacket_lengths = int(packet[7 : 7 + 15], 2)
        curr_len = 0
        while curr_len < subpacket_lengths:
            subpacket_len, subpacket = parse_packet(packet[7 + 15 + curr_len :])
            curr_len += subpacket_len
            subpackets.append(subpacket)
        assert curr_len == subpacket_lengths
        return 7 + 15 + curr_len, Packet(
            version=version, p_type=type_id, data=subpackets
        )
    elif packet[6] == "1":
        n_subpackets = int(packet[7 : 7 + 11], 2)
        curr_len = 0
        for _ in range(n_subpackets):
            subpacket_len, subpacket = parse_packet(packet[7 + 11 + curr_len :])
            curr_len += subpacket_len
            subpackets.append(subpacket)
        return 7 + 11 + curr_len, Packet(
            version=version, p_type=type_id, data=subpackets
        )


def read_number(packet):
    i = 0
    num = ""
    while packet[i] == "1":
        num += packet[i + 1 : i + 5]
        i += 5
    num += packet[i + 1 : i + 5]
    i += 5
    return i, int(num, 2)


def sum_version(packet: Packet):
    if packet.p_type == 4:
        return packet.version
    else:
        return packet.version + sum(sum_version(subpacket) for subpacket in packet.data)


def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = parse_data(data)
    _, packet = parse_packet(data)

    print("Part 1")
    version_sum = sum_version(packet)
    print(f"The sum of all version numbers of all packets is {version_sum}")
    print()

    print("Part 2")
    value = packet.compute_value()
    print(f"The value of the outermost package in the BITS transmission is {value}")
    print()


if __name__ == "__main__":
    main()
