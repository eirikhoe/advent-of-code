import numpy as np

with open("input.txt", "r") as file:
    pixels = [int(pixel) for pixel in file.read().strip()]

image = np.reshape(pixels, (-1, 6, 25))
least_zero_layer = np.argmin(np.sum(image == 0, axis=(1, 2)))
result = np.sum(image[least_zero_layer] == 1) * np.sum(image[least_zero_layer] == 2)
print(result)
