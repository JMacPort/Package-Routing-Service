# The package class will be used to create and manage packages. It also creates a format for where the string can be
# viewed cohesively.

# The entire class has a time and space complexity of O(1)
class Package:

    def __init__(self, id, address, city, state, zip, deadline, weight, notes):
        """Creates a package object and stores necessary information about each package"""
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.weight = weight
        if notes == "":
            self.notes = "N/A"
        else:
            self.notes = notes
        self.status = "In hub"
        self.delivery_time = ""
        self.leave_time = ""
        self.truck_number = ""

    def get_package(self):
        """Returns the contents of the package in a formatted string"""
        return (f"ID: {self.id:<2} | ADDRESS: {self.address:<38} | CITY: {self.city:<17} | STATE: {self.state:<2} | "
                f"ZIP: {self.zip:<5} | DEADLINE: {self.deadline:<8} | WEIGHT (in kilos): {self.weight:>4} | STATUS: "
                f"{self.status:<25}")

    def change_status(self, time):
        """Used when a package status is needed upon request of a given time. Will return either
        'En route', 'Delivered' or 'At the hub'"""
        if time < self.leave_time:
            self.status = f"({time}) At the hub"
        elif time > self.delivery_time:
            self.status = f"({time}) Delivered at {self.delivery_time} by Truck {self.truck_number}"
        else:
            self.status = f"({time}) En route on truck {self.truck_number}"
