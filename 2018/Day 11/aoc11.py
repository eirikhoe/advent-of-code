from pathlib import Path
import numpy as np

def main():
    serial = 8141
    print(find_best_square(serial,3))
    print(find_best_square(serial))


def find_best_square(serial,square_size=None):
    size = 300
    gen = np.arange(size)+1
    X = np.tile(gen,(size,1))
    Y = np.copy(X.T)
    p = X+10
    p *= Y
    p += serial
    p *= (X+10)
    p = (p % 1000)//100
    p -= 5
    max_power = -1000
    if square_size is None:
        square_sizes = range(1,size+1)
    else:
        square_sizes = [square_size]
    for square_size in square_sizes:
        for y in range(size-square_size):
            for x in range(size-square_size):
                total_power = np.sum(p[y:y+square_size,x:x+square_size])
                if total_power > max_power:
                    best_square = (x+1,y+1,square_size)
                    max_power = total_power
    return best_square

if __name__ == "__main__":
    main()