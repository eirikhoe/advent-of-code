import numpy as np


def find_crossing_times(first_seg, second_seg):

    # Is the first segment vertical
    if first_seg[0, 0] == first_seg[0, 1]:
        # Is the second segment vertical
        if second_seg[0, 0] == second_seg[0, 1]:

            # Only way to have intersection is if x-coordinates match
            if second_seg[0, 0] == first_seg[0, 0]:
                coords_y = np.arange(
                    max(first_seg[1].min(), second_seg[1].min()),
                    min(first_seg[1].max(), second_seg[1].max()) + 1,
                )
                coords_x = np.full(coords_y.size, first_seg[0, 0], dtype=int)
                first_len = first_seg[2,0]+np.abs(first_seg[1,0]-coords_y)
                second_len = second_seg[2,0]+np.abs(second_seg[1,0]-coords_y)

                return np.array([first_len, second_len])
            else:
                return None
        else:

            # Check for possible crossing point when second segment is horisontal
            if (
                first_seg[0, 0] >= second_seg[0].min()
                and first_seg[0, 0] <= second_seg[0].max()
                and second_seg[1, 0] >= first_seg[1].min()
                and second_seg[1, 0] <= first_seg[1].max()
            ):
                first_len = first_seg[2,0]+np.abs(first_seg[1,0]-second_seg[1,0])
                second_len = second_seg[2,0]+np.abs(second_seg[0,0]-first_seg[0,0])

                return np.reshape([first_len, second_len],(2,1))
            else:
                return None

    # First segment is horisontal
    else:
        # Check if second segment is horisontal
        if second_seg[1, 0] == second_seg[1, 1]:

            # Only way to have intersection is if y-coordinates match
            if second_seg[1, 0] == first_seg[1, 0]:
                coords_x = np.arange(
                    max(first_seg[0].min(), second_seg[0].min()),
                    min(first_seg[0].max(), second_seg[0].max()) + 1,
                )
                coords_y = np.full(coords_x.size, first_seg[1, 0], dtype=int)
                first_len = first_seg[2,0]+np.abs(first_seg[0,0]-coords_x)
                second_len = second_seg[2,0]+np.abs(second_seg[0,0]-coords_x)

                return np.array([first_len, second_len])
            else:
                return None
        else:

            # Check for possible crossing point when second segment is vertical
            if (
                first_seg[1, 0] >= second_seg[1].min()
                and first_seg[1, 0] <= second_seg[1].max()
                and second_seg[0, 0] >= first_seg[0].min()
                and second_seg[0, 0] <= first_seg[0].max()
            ):
                first_len = first_seg[2,0]+np.abs(first_seg[0,0]-second_seg[0,0])
                second_len = second_seg[2,0]+np.abs(second_seg[1,0]-first_seg[1,0])

                return np.reshape([first_len, second_len],(2,1))
            else:
                return None


wires = []
with open("input.txt", "r") as file:
    for line in file:
        wires.append(line.strip().split(","))

for i, wire in enumerate(wires):
    wire_points = np.zeros((3, 1), dtype=int)
    for segment in wire:
        direction = segment[0]
        length = int(segment[1:])
        if direction == "L":
            new_point_x = wire_points[0, -1] + length
            new_point_y = wire_points[1, -1]
        elif direction == "R":
            new_point_x = wire_points[0, -1] - length
            new_point_y = wire_points[1, -1]
        elif direction == "U":
            new_point_x = wire_points[0, -1]
            new_point_y = wire_points[1, -1] + length
        elif direction == "D":
            new_point_x = wire_points[0, -1]
            new_point_y = wire_points[1, -1] - length
        wire_len = wire_points[2, -1] + length
        wire_points = np.append(
            wire_points,
            np.reshape([new_point_x, new_point_y, wire_len], (3, 1)),
            axis=1,
        )
    wires[i] = wire_points

min_crossing_point_time = np.inf
for i in range(wires[0].shape[1] - 1):
    for j in range(wires[1].shape[1] - 1):
        add_points = find_crossing_times(wires[0][:, i : i + 2], wires[1][:, j : j + 2])
        if add_points is not None:
            for k in range(add_points[0].size):
                dist = np.sum(add_points[:, k])
                if (dist > 0) and (dist < min_crossing_point_time):
                    min_crossing_point_time = dist

print(min_crossing_point_time)
