import numpy as np

def look_and_say(seq):
    count = 1
    res = []
    for i in range(len(seq)-1):
        if seq[i] == seq[i+1]:
            count += 1
        else:
            res.append(count)
            res.append(seq[i])
            count = 1
    res.append(count)
    res.append(seq[-1])
    return res

def rep_look_and_say(seq,n_repeats):
    seq = [int(d) for d in seq]
    for i in range(n_repeats):
        seq = look_and_say(seq)

    return "".join([str(d) for d in seq])

def main():
    seq = "1321131112"

    print("Part 1")
    len_res = len(rep_look_and_say(seq,40))
    print(f"The length of the result is {len_res} characters")
    print()


    print("Part 2")
    len_res = len(rep_look_and_say(seq,50))
    print(f"The length of the result is {len_res} characters")



if __name__ == "__main__":
    main()
