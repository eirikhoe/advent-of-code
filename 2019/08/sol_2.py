import numpy as np

with open("day_8_input.txt", "r") as file:
    pixels = [int(pixel) for pixel in file.read().strip()]

image_size = [6, 25]
image = np.reshape(pixels, (-1, image_size[0], image_size[1]))

layers = np.argmax(image < 1.5, axis=0)

print(
    image[
        layers,
        np.tile(np.arange(image_size[0]), (image_size[1], 1)).T,
        np.tile(np.arange(image_size[1]), (image_size[0], 1)),
    ]
)
