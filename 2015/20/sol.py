def find_presents(house_number):
    divisible = []
    i = 1
    while i * i <= house_number:
        if (house_number % i) == 0:
            d = house_number // i
            divisible.append(i)
            if i != d:
                divisible.append(d)
        i += 1
    return sum(divisible) * 10


def find_presents_alt(house_number):
    divisible = []
    i = 1
    while i <= min(50, house_number):
        if (house_number % i) == 0:
            d = house_number // i
            divisible.append(d)
        i += 1
    return sum(divisible) * 11


def find_lowest_house_number(target, alt=False):
    method = {False: find_presents, True: find_presents_alt}
    house_number = 1
    p = method[alt](house_number)
    while p < target:
        house_number += 1
        p = method[alt](house_number)
    return house_number


def main():
    target = 36000000
    print("Part 1")
    num = find_lowest_house_number(target)
    print(f"The lowest house number to get at least {target} presents is house {num}")
    print()

    print("Part 2")
    num = find_lowest_house_number(target, alt=True)
    print(f"The lowest house number to get at least {target} presents is house {num}")


if __name__ == "__main__":
    main()
