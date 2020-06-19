import math


# Calculate distance between two star systems in light years using their x, y & z coordinates
def calculate_distance(x1, y1, z1, x2, y2, z2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2 + (z1 - z2) ** 2)


# Calculate distance from current system to destination system
# As a percentage of the distance from origin system to destination system
def calculate_percentage(ori_to_dest, curr_to_dest, decimal_places=2):
    invert_curr_to_dest = ori_to_dest - curr_to_dest
    return round(invert_curr_to_dest / ori_to_dest * 100, decimal_places)
