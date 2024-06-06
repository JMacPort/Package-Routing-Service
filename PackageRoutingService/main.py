# Import from my 3 custom classes and the csv/datatime libraries
from hashtable import HashTable
from package import Package
from truck import Truck
import datetime
import csv

# Creating objects from the classes that were imported
ht = HashTable(40)
# Truck 1 was able to leave immediately and was not waiting on any additional packages
truck1 = Truck(1, datetime.timedelta(hours=8))

# Truck 2 was set to leave when package ID 9, was updated and truck 1 was back.
truck2 = Truck(2, datetime.timedelta(hours=10, minutes=20))

# Truck 3 left when any delayed packages arrived at the hub
truck3 = Truck(3, datetime.timedelta(hours=9, minutes=5))

# Set the main hub address for ease of accessibility
HUB_ADDRESS = '4001 South 700 East'

# Opens the package CSV and inputs each attribute into a package object
with open("packages.csv") as packages:
    reader = csv.DictReader(packages)
    for item in reader:
        package = Package(item['PackageID'], item['Address'], item['City'], item['State'], item['Zip'],
                          item['Delivery Deadline'], item['Weight KILO'], item['page 1 of 1PageSpecial Notes'])
        # Inserts package object into the hash table using the packageID as the key
        ht.insertion(int(item['PackageID']), package)

# Load the trucks with the packages based on the package specifications
truck1.packages = [1, 4, 5, 13, 14, 15, 16, 19, 20, 29, 30, 31, 34, 37, 40]
truck2.packages = [2, 3, 8, 9, 10, 12, 18, 23, 25, 26, 33, 35, 36, 38]
truck3.packages = [6, 7, 11, 17, 21, 22, 24, 27, 28, 32, 39]

# Reads the CSV containing addresses and stores each in a list for later use
with open("cleaned_address.csv") as csv_address:
    addresses = list(csv.reader(csv_address))

# Opens the CSV containing a distance matrix which holds the distances from each location
with open("cleaned_distance.csv") as csv_distance:
    distances = list(csv.reader(csv_distance))


def get_distance(starting, ending):
    """When provided with a starting and ending index it will search through the 2d array and return the distance value
    that is at the given location in the array. If the given index does not return a number, the entries are swapped
    to ensure that a data point is found. It is then returned as a float value."""
    distance = distances[starting][ending]
    if distance == '':
        distance = distances[ending][starting]
    return float(distance)


def address_index(street):
    """When given a street name, it will loop through the addresses and return the index of the address that was
    created from the given csv"""
    for address in addresses:
        if address == street:
            return addresses.index(street)


# This contains my algorithm for package drop off, using a nearest neighbor variant it will deliver the next closest
# package determined by the distance from two addresses
def drop_off(truck):
    """The drop_off function takes a truck as input and initializes a new list of packages based on the ids passed in
    originally. It will then loop through each package in its truck and assign a truck number and a leave time to each
    package, which is set to the truck time when the object was created. Then, while the truck still contains packages
    it sets the distance to a large number and the current package to a blank string. Looping through each package, it
    checks to make sure the package doesn't have the wrong address and then finds the shortest distance to the next
    address. It then updates the truck and package attributes to reflect the delivered package. When all packages are
    delivered, the truck is sent back to the hub and adjusted accordingly"""
    truck.packages = [ht.look_up(p_id) for p_id in truck.packages]
    for item in truck.packages:
        item.truck_number = truck.number
        item.status = f"Loaded onto truck {truck.number} at {truck.time}"
        item.leave_time = truck.time

    while len(truck.packages) != 0:
        short_distance = 10000
        curr_package = ''

        # This begins my nearest neighbor algorithm
        for item in truck.packages:
            # This check will only be true with Truck 2, and since it leaves at the time it is able to freely update
            if item.id == "9":
                item.address = "410 S State St"
            index_address = addresses.index([truck.current_stop])
            package_index = addresses.index([item.address])
            distance = get_distance(index_address, package_index)
            if distance < short_distance:
                short_distance = distance
                curr_package = item
        # This ends my nearest neighbor algorithm

        truck.deliver(curr_package)
        truck.miles_driven += short_distance
        truck.current_stop = curr_package.address
        truck.time += datetime.timedelta(hours=short_distance / truck.speed)
        curr_package.delivery_time = truck.time
        curr_package.status = f"Delivered at {curr_package.delivery_time} by truck {truck.number}"

    index_address = addresses.index([truck.current_stop])
    hub_index = addresses.index([HUB_ADDRESS])
    distance = get_distance(index_address, hub_index)
    truck.time += datetime.timedelta(hours=distance / truck.speed)
    truck.current_stop = HUB_ADDRESS


# Since truck1 will always be back before truck2 in this case, truck2 is able to deliver packages without constraints
drop_off(truck1)
drop_off(truck3)
drop_off(truck2)

total_mileage = truck1.miles_driven + truck2.miles_driven + truck3.miles_driven


# This is what will run when the program starts. It will ask the user multiple questions and return information
# based on their input. There are processes to return the miles driven, all or a single package status/es at a given
# time, and if a user would like to rerun the program.
class Main:
    program_running = True
    while program_running:

        show_miles = input("Would you like to see the total miles driven by the trucks? Enter Y/N: ")
        if show_miles.upper() == 'Y':
            # Prints the total amount of miles that the trucks took to deliver all the packages.
            # In my case it was 99.7 miles.
            print(f'This route took the trucks: {total_mileage:.2f} miles.')
            print(f'Truck 1: {truck1.miles_driven}')
            print(f'Truck 2: {truck2.miles_driven}')
            print(f'Truck 3: {truck3.miles_driven}\n')

        # Ask the user to input a time, if in the correct format it will accept. Otherwise, the program will restart
        user_time = input("Provide a time in a 24-HR format (Hours:Minutes:Seconds): ")
        try:
            hours, minutes, seconds = user_time.split(":")
            user_time = datetime.timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        except ValueError:
            print("Invalid Input... Restarting\n")
            continue

        # Asks the user how many packages they would like to view, if an invalid entry, the program will restart
        package_amount = input("Type 'ALL' if you would like to see all package status, "
                               "or type 'SINGLE' if just a single package should be shown: ")

        # The package is checked and updated accordingly based on the given user time as long as the input was valid
        if package_amount.upper() == "ALL":
            for package in ht.get_all():
                package.change_status(user_time)
                print(package.get_package())
        elif package_amount.upper() == "SINGLE":
            user_package = int(input("Please enter the ID of the package in numerical form: "))
            if user_package > len(ht.get_all()) or user_package < 1:
                print("Invalid Package... Restarting\n")
                continue
            new_package = ht.look_up(user_package)
            new_package.change_status(user_time)
            print(new_package.get_package())
        else:
            print("Invalid entry.... Restarting\n")
            continue

        print()
        print()

        # Asks the user if they would like to run the program again. Any response other than 'N' will cause a restart.
        do_continue = input("Do you want to run the program again? Enter Y/N: ")
        if do_continue.upper() == "N":
            program_running = False
        elif do_continue.upper() == "Y":
            pass
        else:
            print("Invalid entry.... Restarting\n")
            continue
