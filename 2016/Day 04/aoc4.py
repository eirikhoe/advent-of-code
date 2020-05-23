from pathlib import Path
import re
import numpy as np

data_folder = Path(".").resolve()

reg = re.compile(r"((?:[a-z]+\-)+)(\d+)\[([a-z]{5})\]")


class Room:
    def __init__(self,encryped_name,sector_id,checksum):
        self.encryped_name = encryped_name
        self.sector_id = sector_id
        self.checksum = checksum
        self.decrypted_name = None

    def valid(self):
        room_chars = np.array([ord(char) for char in "".join(self.encryped_name.split('-'))],dtype=int)
        unique_chars, counts = np.unique(room_chars, return_counts=True)
        index = np.lexsort((unique_chars,-counts))
        valid_checksum = "".join([chr(i) for i in unique_chars[index[:5]]])
        
        return self.checksum == valid_checksum

    def decrypt(self):
        self.decrypted_name = ""
        for letter in self.encryped_name:
            if letter == '-':
                self.decrypted_name += " "
            else:
                self.decrypted_name += self.shift(letter)

    def shift(self,letter):
        alphabet_index = ord(letter)-ord('a')
        new_index = (alphabet_index+self.sector_id) % 26
        new_letter = chr(new_index + ord('a'))
        return new_letter


class Rooms:

    def __init__(self,data):
        self.rooms = []
        for line in data.split("\n"):
            m = reg.match(line)
            encryped_name = m.group(1)[:-1]
            sector_id = int(m.group(2))
            checksum = m.group(3)
            self.rooms.append(Room(encryped_name,sector_id,checksum))
        self.valid_rooms = []
        self._find_valid_rooms()    


    def sum_valid_sector_ids(self): 
        sum_sector_id = 0
        for room_nr in self.valid_rooms:
            sum_sector_id += self.rooms[room_nr].sector_id
        return sum_sector_id

    def _find_valid_rooms(self): 
        for i,room in enumerate(self.rooms):
            if room.valid():
                self.valid_rooms.append(i) 

    def print_decrypted_room_names(self):
        decrypted_names = []
        for room_nr in self.valid_rooms:
            room = self.rooms[room_nr] 
            room.decrypt()
            decrypted_names.append(f"{room.decrypted_name} {room.sector_id}")
        print("\n".join(decrypted_names))

    def find_north_pole_storage(self):
        for room_nr in self.valid_rooms:
            room = self.rooms[room_nr] 
            room.decrypt()
            if "north" in room.decrypted_name:
                return room.decrypted_name, room.sector_id


def main():
    data = data_folder.joinpath("input.txt").read_text()
    r = Rooms(data)
    
    print("Part 1")
    print(f"The sum of the sector IDs for the real rooms is {r.sum_valid_sector_ids()}")
    print()

    print("Part 2")
    room,sector_id = r.find_north_pole_storage()
    print(f"The sector ID of the room, {room}, where North Pole objects are stored is {sector_id}")
    
if __name__ == "__main__":
    main()
