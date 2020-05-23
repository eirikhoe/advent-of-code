count = 0
for number in range(146810, 612564 + 1):
    digits = [int(d) for d in str(number)]
    nondecreasing = True
    equal_counter = []
    equal_count = 1
    for j in range(len(digits) - 1):
        if digits[j] == digits[j + 1]:
            equal_count += 1
            if j == len(digits) - 2:
                equal_counter.append(equal_count)
        else:
            equal_counter.append(equal_count)
            equal_count = 1

        if digits[j] > digits[j + 1]:
            nondecreasing = False
    if (2 in equal_counter) and nondecreasing:
        count += 1

print(count)

