# Standalone program for Exploration Progress
from system import System
import calculate


def get_system_name(prompt):
    user_input = str(input(prompt))
    return user_input


print("Exploration Progress by Dlljs")
origin = System()
origin.setName(name=get_system_name("Enter the name of the origin system: "), populate=True)
destination = System()
destination.setName(name=get_system_name("Enter the name of the destination system: "), populate=True)
current = System()
current.setName(name=get_system_name("Enter the name of the system you are currently at: "), populate=True)

origin_coords = origin.getCoords()
destination_coords = destination.getCoords()
current_coords = current.getCoords()
ori_to_dest_distance = calculate.calculate_distance(origin_coords["x"],
                                                    origin_coords["y"],
                                                    origin_coords["z"],
                                                    destination_coords["x"],
                                                    destination_coords["y"],
                                                    destination_coords["z"])
curr_to_dest_distance = calculate.calculate_distance(current_coords["x"],
                                                     current_coords["y"],
                                                     current_coords["z"],
                                                     destination_coords["x"],
                                                     destination_coords["y"],
                                                     destination_coords["z"])
percentage = calculate.calculate_percentage(ori_to_dest_distance,curr_to_dest_distance)
print("You are " + str(percentage) + "% of the way there!")
