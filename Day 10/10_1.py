from pathlib import Path

import numpy as np

data_folder = Path(".")

file = data_folder / "day_10_input.txt"
instrs = [[int(d) for d in list(x)] for x in file.read_text().replace('.','0').replace('#','1').split('\n')]

print(instrs)