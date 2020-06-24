# Standalone program for Exploration Progress
from system import System
import calculate


def get_system_name(system_object, prompt):
    input_system = True
    while input_system:
        user_input = str(input(prompt))
        system_object.setName(name=user_input, verify=True, populate=True)
        if system_object.getNameVerified():
            input_system = False
        else:
            input_system = True
            print("Error: Could not get data on the " + str(user_input) + " system in the EDSM database.")
            print("Either it does not exist, or there was a problem connecting.")


print("Exploration Progress by Dlljs")
origin = System()
destination = System()
current = System()
get_system_name(origin, "Enter the name of the origin system: ")
get_system_name(destination, "Enter the name of the destination system: ")
get_system_name(current, "Enter the name of the system you are currently at: ")

origin_coords = origin.getCoords()
destination_coords = destination.getCoords()
current_coords = current.getCoords()
percentage = calculate.calculate_progress(origin_coords, current_coords, destination_coords)
print("You are " + str(percentage) + "% of the way there!")
