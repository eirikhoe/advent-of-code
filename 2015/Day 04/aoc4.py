from hashlib import md5

def lowest_zero_number(key,n_zeros):
    i = 1
    while True:
        hashed_string = md5(f"{key}{i}".encode("utf-8")).hexdigest()
        if hashed_string[:n_zeros] == "0"*n_zeros:
            return i
        i += 1

def main():
    key = "bgvyzdsv"
    
    print("Part 1")
    print(f"The lowest number with a five zero hash is {lowest_zero_number(key,5)}")
    print()

    print("Part 2")
    print(f"The lowest number with a six zero hash is {lowest_zero_number(key,6)}")
    
if __name__ == "__main__":
    main()
