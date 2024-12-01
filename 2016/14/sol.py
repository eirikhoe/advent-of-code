from hashlib import md5
from collections import deque


def gen_keys(salt, hash_stretching=False):
    i = 0
    n_keys = 0
    key_lim = 64
    future_fives = deque([])
    past_threes = deque([])
    while n_keys < key_lim:
        hashed_string = md5(f"{salt}{i}".encode("utf-8")).hexdigest()
        if hash_stretching:
            for j in range(2016):
                hashed_string = md5(hashed_string.encode("utf-8")).hexdigest()

        counter = 1
        three = None
        fives = []
        for j in range(1, len(hashed_string)):
            if hashed_string[j] == hashed_string[j - 1]:
                counter += 1
            else:
                counter = 1
            stops = (j == (len(hashed_string) - 1)) or (
                hashed_string[j + 1] != hashed_string[j]
            )
            if (counter == 3) and (three is None):
                three = hashed_string[j]
            if counter == 5:
                fives.append(hashed_string[j])
        future_fives.append(list(set(fives)))
        past_threes.append(three)
        if i >= 1000:
            future_fives.popleft()
            past_three = past_threes.popleft()
            for future_five in future_fives:
                if past_three in future_five:
                    n_keys += 1
                    break

        i += 1

    return i - 1001


def main():
    salt = "ahsbgdzn"
    print("Part 1")
    print(f"Index {gen_keys(salt)} generates the 64th one-time pad key")
    print()

    print("Part 2")
    print(
        f"With hash-stretching activated index {gen_keys(salt,True)} generates the 64th one-time pad key"
    )


if __name__ == "__main__":
    main()
