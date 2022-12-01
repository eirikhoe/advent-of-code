count = 0
for number in range(146810, 612564 + 1):
    digits = [int(d) for d in str(number)]
    two_in_row = False
    nondecreasing = True
    for j in range(5):
        if digits[j] == digits[j + 1]:
            two_in_row = True
        if digits[j] > digits[j + 1]:
            nondecreasing = False
    if two_in_row and nondecreasing:
        count += 1

print(count)

