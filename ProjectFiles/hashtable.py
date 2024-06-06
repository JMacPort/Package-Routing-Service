# Creates a hash table with a size set to 40, with all cells currently empty.
# Contains insertion and look up functions as well.

# The table has a  Space Complexity of O(n)
class HashTable:

    # Time Complexity - O(n)
    def __init__(self, size):
        """Creates a hash table with a size of 40 and maps each cell of the array to None"""
        self.size = size
        self.map = [None] * self.size

    # Time Complexity - O(1)
    def hash(self, key):
        """Creates a hash value for the given key (the package ID)"""
        return key % self.size

    # Time Complexity - O(1)
    def insertion(self, key, items):
        """Inserts a new list of items (the package) at a given hashed key index"""
        new_hash = self.hash(key)
        self.map[new_hash] = items

    # Time Complexity - O(1)
    def look_up(self, key):
        """Returns a specific package object with a given ID"""
        new_hash = self.hash(key)
        return self.map[new_hash]

    # Time Complexity - O(n)
    def get_all(self):
        """Returns a list of all package objects current stored in the hash table"""
        all_packages = []
        for i in range(1, self.size + 1):
            all_packages.append(self.look_up(i))
        return all_packages
