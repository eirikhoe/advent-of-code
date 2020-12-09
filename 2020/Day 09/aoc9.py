from pathlib import Path


def find_factors(entries, total, n_factors):
    if n_factors == 1:
        if total in entries:
            return [total]
        else:
            return None

    for i, entry in enumerate(entries[:-1]):
        factors = find_factors(entries[i + 1 :], total - entry, n_factors - 1)
        if factors:
            factors.append(entry)
            return factors
    return None


def find_invalid(numbers, preamble_len):
    for i in range(preamble_len, len(numbers)):
        preamble = numbers[i - preamble_len : i].copy()
        if find_factors(preamble, numbers[i], 2) is None:
            return numbers[i]
    return None


def find_weakness(numbers, target):
    n = len(numbers)
    for i in range(n):
        j = i + 1
        sum = numbers[i]
        while (j < n) and (sum < target):
            sum += numbers[j]
            j += 1
        if sum == target:
            return min(numbers[i:j]) + max(numbers[i:j])
    return None


def main():
    data_folder = Path(".").resolve()
    data = data_folder.joinpath("input.txt").read_text()
    data = [int(d) for d in data.split("\n")]
    target = find_invalid(data, 25)
    print("Part 1:")
    print(f"The first number without this property is {target}")
    print()

    print("Part 2:")
    weakness = find_weakness(data, target)
    print(f"The encryption weakness is {weakness}")


if __name__ == "__main__":
    main()
