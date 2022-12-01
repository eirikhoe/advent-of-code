from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    data = [line for line in data.split("\n")]
    return data


def find_power_consumption(data):
    gamma_str = ""
    epsilon_str = ""
    number_len = len(data[0])
    n_numbers = len(data)
    for i in range(number_len):
        n_ones = 0
        for line in data:
            n_ones += line[i] == "1"
        if n_ones > (n_numbers / 2):
            gamma_str += "1"
            epsilon_str += "0"
        elif n_ones < (n_numbers / 2):
            gamma_str += "0"
            epsilon_str += "1"
    gamma_rate = int(gamma_str, 2)
    epsilon_rate = int(epsilon_str, 2)
    power_consumption = gamma_rate * epsilon_rate
    return power_consumption


def find_rating(data, rating_type):
    data = data.copy()
    number_len = len(data[0])
    for i in range(number_len):
        n_ones = 0
        n_numbers = len(data)
        if n_numbers == 1:
            break
        ones_indices = []
        zeros_indicies = []
        for j in range(n_numbers):
            if data[j][i] == "1":
                ones_indices.append(j)
            else:
                zeros_indicies.append(j)
        n_ones = len(ones_indices)

        if (rating_type == "co2") ^ (n_ones >= (n_numbers / 2)):
            del_indicies = zeros_indicies
        else:
            del_indicies = ones_indices
        for k in reversed(del_indicies):
            data.pop(k)
    return int(data[0], 2)


def find_life_support_rating(data):
    co2_scrubber_rating = find_rating(data, "co2")
    oxygen_generator_rating = find_rating(data, "oxygen")
    life_support_rating = co2_scrubber_rating * oxygen_generator_rating
    return life_support_rating


def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = parse_data(data)

    print("Part 1")
    power_consumption = find_power_consumption(data)
    print(f"The power consumption is {power_consumption}")
    print()

    print("Part 2")
    life_support_rating = find_life_support_rating(data)
    print(f"The life support rating is {life_support_rating}")
    print()


if __name__ == "__main__":
    main()
