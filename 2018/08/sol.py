from pathlib import Path
import numpy as np
import re
from collections import defaultdict


class License:
    def __init__(self, file):
        self.file = file
        self.first_check = 0
        self._index = 0
        self._compute_first_check()
        self._index = 0
        self.second_check = self._compute_second_check()

    def _compute_first_check(self):
        n_children = self.file[self._index]
        self._index += 1
        n_meta = self.file[self._index]
        self._index += 1
        for i in range(n_children):
            self._compute_first_check()
        self.first_check += sum(self.file[self._index : self._index + n_meta])
        self._index += n_meta

    def _compute_second_check(self):
        n_children = self.file[self._index]
        self._index += 1
        n_meta = self.file[self._index]
        self._index += 1
        children_value = []
        for i in range(n_children):
            children_value.append(self._compute_second_check())

        if n_children == 0:
            value = sum(self.file[self._index : self._index + n_meta])
            self._index += n_meta
        else:
            value = 0
            for i in range(n_meta):
                meta = self.file[self._index]
                self._index += 1
                if 0 < meta <= n_children:
                    value += children_value[meta - 1]

        return value


def main():
    data_folder = Path(".").resolve()
    text = data_folder.joinpath("input.txt").read_text()
    data = [int(d) for d in text.split(" ")]
    license = License(data)
    print(license.first_check)
    print(license.second_check)


if __name__ == "__main__":
    main()
