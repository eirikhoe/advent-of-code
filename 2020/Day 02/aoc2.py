from pathlib import Path
import numpy as np
import re
data_folder = Path(".").resolve()

reg_password = re.compile(r"(\d+)-(\d+) ([a-z]): ([a-z]+)")

def get_password_info(password_info):
    match = reg_password.match(password_info)
    int_1 = int(match.groups()[0])
    int_2 = int(match.groups()[1])
    char = match.groups()[2]
    pwd = match.groups()[3]
    return int_1, int_2, char, pwd

def is_password_valid_sled(password_info):
    min_count, max_count, char, pwd = get_password_info(password_info)
    char_count = pwd.count(char)
    return min_count <= char_count <= max_count

def is_password_valid_toboggin(password_info):
    index_1, index_2, char, pwd = get_password_info(password_info)
    index_1 -= 1
    index_2 -= 1
    return (pwd[index_1] == char) != (pwd[index_2] == char) 

def get_n_valid_passwords(passwords_info, policy_type):
    n_valid_passwords = 0
    for password_info in passwords_info:
        if policy_type == "sled":
            n_valid_passwords += is_password_valid_sled(password_info)
        elif policy_type == "toboggin":
            n_valid_passwords += is_password_valid_toboggin(password_info)
        else:
            raise RuntimeError("Unknown policy type")
    
    return n_valid_passwords

def main():
    data = data_folder.joinpath("input.txt").read_text()
    data = data.split("\n")
    
    print("Part 1")
    n = get_n_valid_passwords(data,"sled")
    print(f"There are {n} valid passwords in the list when using sled policies")
    print()

    print("Part 2")
    n = get_n_valid_passwords(data,"toboggin")
    print(f"There are {n} valid passwords in the list when using toboggin policies")


if __name__ == "__main__":
    main()
