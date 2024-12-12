from pathlib import Path

data_folder = Path(".").resolve()


def parse_data(data):
    disk_map = [int(d) for d in data]
    return disk_map


def make_disk(disk_map):
    blocks = [0 for _ in range(sum(disk_map))]
    block_ind = 0
    i = 0
    files = []
    while i < len(blocks):
        if block_ind % 2 == 0:
            val = block_ind // 2
            files.append((i, disk_map[block_ind]))
        else:
            val = -1
        start = i
        i += disk_map[block_ind]
        blocks[start:i] = [val for _ in range(disk_map[block_ind])]
        block_ind += 1
    return blocks, files


def compact(disk_map, whole_files):
    blocks, files = make_disk(disk_map)
    file_ind = len(files) - 1
    while file_ind >= 0:
        space = False
        space_count = 0
        file = files[file_ind]
        for ind in range(file[0] + 1):
            if blocks[ind] == -1:
                space_count += 1
                space = True
                if whole_files and (space_count >= file[1]):
                    blocks[ind - space_count + 1 : ind + 1] = blocks[
                        file[0] : file[0] + file[1]
                    ]
                    blocks[file[0] : file[0] + file[1]] = [-1 for _ in range(file[1])]
                    file_ind -= 1
                    break
            else:
                if (space_count > 0) and (not whole_files):
                    l = min(space_count, file[1])
                    files[file_ind] = (files[file_ind][0], files[file_ind][1] - l)
                    blocks[ind - space_count : ind - space_count + l] = blocks[
                        file[0] + file[1] - l : file[0] + file[1]
                    ]
                    blocks[file[0] + file[1] - l : file[0] + file[1]] = [
                        -1 for _ in range(l)
                    ]
                    if files[file_ind][1] == 0:
                        file_ind -= 1
                    break
                space_count = 0
        else:
            file_ind -= 1
            if not space:
                return blocks
    return blocks


def compute_checksum(blocks):
    return sum(id * i for i, id in enumerate(blocks) if id > 0)


def compute_compacted_checksum(disk_map, whole_files):
    blocks = compact(disk_map, whole_files)
    return compute_checksum(blocks)


def main():
    data = data_folder.joinpath("input.txt").read_text().rstrip()
    disk_map = parse_data(data)

    print("Part 1")
    checksum = compute_compacted_checksum(disk_map, False)
    print(f"The checksum is {checksum}.")
    print()

    print("Part 2")
    checksum = compute_compacted_checksum(disk_map, True)
    print(f"The checksum when moving whole files is {checksum}.")
    print()


if __name__ == "__main__":
    main()
