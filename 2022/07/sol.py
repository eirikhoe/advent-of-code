from pathlib import Path
from dataclasses import dataclass
from typing import Optional, List


data_folder = Path(".").resolve()


@dataclass
class Folder:
    name: str
    file_size: int
    parent: Optional[int]
    children: List[int]
    know_content: bool = False
    total_dir_size = 0


def parse_data(data):
    lines = [line.strip() for line in data.split("\n")]
    if lines[0] != "$ cd /":
        raise RuntimeError("Must intially cd to root")
    folders = [Folder("/", 0, None, [])]
    curr = 0
    ind = 1
    while ind < len(lines):
        if lines[ind].startswith("$ cd"):
            directory = lines[ind][5:]
            if directory == "..":
                curr = folders[curr].parent
            else:
                for i in folders[curr].children:
                    if directory == folders[i].name:
                        curr = i
                        break
                else:
                    raise RuntimeError("Unknown folder")
            ind += 1
        elif lines[ind] == "$ ls":
            ind += 1
            while (ind < len(lines)) and (not lines[ind].startswith("$")):
                if folders[curr].know_content:
                    ind += 1
                    continue
                info, name = lines[ind].split(" ")
                if info == "dir":
                    folders.append(Folder(name, 0, curr, []))
                    folders[curr].children.append(len(folders) - 1)
                else:
                    folders[curr].file_size += int(info)
                ind += 1
            folders[curr].know_content = True
    find_folder_size(folders, 0)
    return folders


def find_folder_size(folders, init_ind):
    size = folders[init_ind].file_size
    for child_ind in folders[init_ind].children:
        find_folder_size(folders, child_ind)
        size += folders[child_ind].total_dir_size
    folders[init_ind].total_dir_size = size


def main():
    data = data_folder.joinpath("input.txt").read_text()
    folders = parse_data(data)

    print("Part 1")
    sum_small_folders = sum(
        [folder.total_dir_size for folder in folders if folder.total_dir_size < 100_000]
    )
    print(f"The small folders have total size {sum_small_folders}")
    print()

    print("Part 2")
    total_size = 70000000
    req_free = 30000000
    used = folders[0].total_dir_size
    minimum_delete = used - (total_size - req_free)
    min_folder_delete = min(
        [folder.total_dir_size for folder in folders if folder.total_dir_size >= minimum_delete]
    )
    print(f"The smallest folder you must delete has size {min_folder_delete}")
    print()


if __name__ == "__main__":
    main()
