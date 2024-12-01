from pathlib import Path
import re
import numpy as np

data_folder = Path(".").resolve()

reg = re.compile(r"\((\d+)x(\d+)\)")


def len_decompressed(text, version=1):
    m = reg.search(text)
    if m is None:
        return len(text)
    else:
        n_chars = int(m.group(1))
        n_repetitions = int(m.group(2))
        span = m.span(0)
        res = span[0] + len_decompressed(text[(span[1] + n_chars) :], version)
        if version == 1:
            res += n_repetitions * len(text[span[1] : (span[1] + n_chars)])
        elif version == 2:
            res += n_repetitions * len_decompressed(
                text[span[1] : (span[1] + n_chars)], version
            )
        return res


def main():
    data = data_folder.joinpath("input.txt").read_text()

    print("Part 1")
    print(f"The decompressed text has length {len_decompressed(data,version=1)}")
    print()

    print("Part 2")
    print(
        f"The decompressed text version two has length {len_decompressed(data,version=2)}"
    )


if __name__ == "__main__":
    main()
