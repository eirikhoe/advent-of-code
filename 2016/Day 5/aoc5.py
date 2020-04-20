from hashlib import md5

def gen_password(door_id):
    password_len = 8
    password = ""
    i = 0
    while len(password) < password_len:
        hashed_string = md5(f"{door_id}{i}".encode("utf-8")).hexdigest()
        if hashed_string[:5] == "00000":
            password += hashed_string[5]
        i += 1
    return password

def gen_inspired_password(door_id):
    password_len = 8
    password = ['_']*password_len
    i = 0
    chars_filled = 0
    while chars_filled < password_len:
        hashed_string = md5(f"{door_id}{i}".encode("utf-8")).hexdigest()
        if hashed_string[:5] == "00000":
            pos = int(hashed_string[5],16)
            if (pos < password_len) and (password[pos] == '_'):
                password[pos] = hashed_string[6]
                print("".join(password))
                chars_filled += 1
        i += 1
    return "".join(password)


def main():
    print("Part 1")
    
    door_id = "reyedfim"
    print(f"The password is {gen_password(door_id)}")
    print()

    print("Part 2")
    print(f"The inspired password is {gen_inspired_password(door_id)}")
    
if __name__ == "__main__":
    main()
