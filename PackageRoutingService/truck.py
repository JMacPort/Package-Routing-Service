# Creates truck objects that take in a set of packages and set various necessary attributes.
class Truck:

    def __init__(self, number, time):
        self.number = number
        self.packages = []
        self.miles_driven = 0
        self.speed = 18
        self.current_stop = "4001 South 700 East"
        self.time = time

    def deliver(self, package):
        """Delivers a package, which removes it from the truck packages list"""
        self.packages.remove(package)


