from edsm import get_coords_from_edsm


class System:  # Represents a star system
    def __init__(self):
        self.name = ""  # Name of this system
        self.coords = {  # Coordinates of this system
            "x": 0,
            "y": 0,
            "z": 0
        }
        self.name_set = False  # True if the system name is locked in
        self.name_verified = True # True if the system name has been verified on EDSM
        self.coords_set = False  # True if the system coordinates are locked in

        # If name is not set, the object is a placeholder until the name is set
        # If coords are not set, but the name is, the coords must be obtained

    # Getters
    def getName(self):
        return self.name

    def getCoords(self):
        return self.coords

    def getNameSet(self):
        return self.name_set

    def getNameVerified(self):
        return self.name_verified

    def getCoordsSet(self):
        return self.coords_set

    # Setters
    def setName(self, name, verify=False, populate=False):
        self.name_set = False
        self.name_verified = False
        self.coords_set = False
        self.name = name
        if self.name == "":
            self.name_set = False
        elif self.name is None:
            self.name_set = False
        else:
            self.name_set = True
            if verify:
                verify_status = self.verifySystem()
                if verify_status:
                    self.name_verified = True
                else:
                    self.name_verified = False
            if populate:
                self.populateCoords()

    def setCoords(self, x, y, z):
        self.coords = {
            "x": x,
            "y": y,
            "z": z
        }
        self.coords_set = True

    # Function to populate coordinates from EDSM
    def populateCoords(self):
        success, x, y, z = get_coords_from_edsm(self.name)
        if success:
            self.setCoords(x, y, z)

    # Function to verify system existence on EDSM
    def verifySystem(self):
        success = get_coords_from_edsm(self.name)
        return success[0]
