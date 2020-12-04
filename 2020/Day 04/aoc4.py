from pathlib import Path
import re

height_re = re.compile(r"(\d+)(in|cm)")
hair_re = re.compile(r"#[0-9a-f]{6}")
pid_re = re.compile(r"^\d{9}$")


def validate_year(passport, field, min_year, max_year):
    if len(passport[field]) != 4:
        return False

    try:
        year = int(passport[field])
    except:
        return False

    return min_year <= year <= max_year


def check_passport_laxed(passport):
    req_fields = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]

    if len(passport) < len(req_fields):
        return False

    for req_field in req_fields:
        if req_field not in passport:
            return False

    return True


def check_passport_strict(passport):
    if not check_passport_laxed(passport):
        return False

    if not validate_year(passport, "byr", 1920, 2002):
        return False

    if not validate_year(passport, "iyr", 2010, 2020):
        return False

    if not validate_year(passport, "eyr", 2020, 2030):
        return False

    try:
        m = height_re.match(passport["hgt"])
        g = m.groups()
        height = int(g[0])
        unit = g[1]
    except:
        return False

    if unit == "cm":
        if (height < 150) or (height > 193):
            return False
    elif (height < 59) or (height > 76):
        return False

    if hair_re.match(passport["hcl"]) is None:
        return False

    eye_colors = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    if passport["ecl"] not in eye_colors:
        return False

    if pid_re.match(passport["pid"]) is None:
        return False

    return True


def count_valid_passports(passports, strict=False):

    n_valid = 0
    for passport in passports:
        if strict:
            n_valid += check_passport_strict(passport)
        else:
            n_valid += check_passport_laxed(passport)
    return n_valid


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    passports = [dict([el.split(":") for el in p.split()]) for p in data.split("\n\n")]

    print("Part 1")
    n_valid = count_valid_passports(passports)
    print(f"In the batch file {n_valid} passports are valid")
    print()

    print("Part 2")
    n_valid = count_valid_passports(passports, strict=True)
    print(f"In the batch file {n_valid} passports are valid with strict checks")
    print()


if __name__ == "__main__":
    main()
