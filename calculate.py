import math


# Calculate distance between two star systems in light years using their x, y & z coordinates
def calculate_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


# Calculate distance from current system to destination system
# As a percentage of the distance from origin system to destination system
def calculate_percentage(ori_to_curr, curr_to_dest, decimal_places=2):
    dist = ori_to_curr + curr_to_dest
    invert_curr_to_dest = dist - curr_to_dest
    return round(invert_curr_to_dest / dist * 100, decimal_places)


# Combines the two functions above into one
# Parameters use dictionaries with three values, with keys being "x", "y" & "z"
def calculate_progress(origin_coords, current_coords, destination_coords):
    origin_to_current = calculate_distance(origin_coords["x"], origin_coords["y"], origin_coords["z"],
                                           current_coords["x"], current_coords["y"], current_coords["z"])
    current_to_destination = calculate_distance(current_coords["x"], current_coords["y"], current_coords["z"],
                                                destination_coords["x"], destination_coords["y"], destination_coords["z"])
    percentage = calculate_percentage(origin_to_current, current_to_destination)
    return percentage
