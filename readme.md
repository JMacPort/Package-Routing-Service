*Screenshots of program running below

# Package Routing
This project was meant to deliver a given number of packages located in the packages.csv file. An algorithm to deliver the package in under a set amount of miles was used to ensure all packages were delivered on time as well as creating the custom objects that would be used. Running the program it will deliver all packages and then the user interface will start 
which will allow the user to input a time to get the status of either all or a single package. From there, the program can either be exited or ran again using a different time/package amount.

## Constraints
- Trucks can contain a maximum of 16 packages.
- All packages must be delivered within 140 miles.
- A hash table must be used to store the packages, which must be custom made.
- A self adjusting algorithm must be used to deliver the packages.
- There are 3 trucks but only 2 drivers, so only 2 trucks may be out at a given time.
- Deliver packages based on the given constraints.

## How I Solved Each
- I custom loaded the trucks based on the special notes section in the package.csv file. This allowed me to meet the constraints but in the future an algorithm should be developed to sort the packages properly.
- The algorithm I implemented was a variation of the nearest neighbor algorithm, and stored the amount of miles from each address to the next in the trucks miles variable.
- I custom created a hash table using no third party libraries. This included functions that hashed the package ID to figure out at which index should the package be stored, inserting packages based on the package ID and the contents of each package, and look up functions to see each package object.
  - I created a package class, where the package attributes could be stored. This would then allow the objects themselves to be stored in trucks and be accessed as needed. Along with the package class, I also created a truck class with a basic deliver function to remove a package from its inventory.
- My nearest neighbor algorithm got the current address index in the cleaned_addresses.csv, along with the next package ID address index. These allowed me to search in the cleaned_distances.csv using both indices and storing this distance.
  - Then, it looped through each package remaining in the trucks packages to find the address that was closest to the current stop. Added that distance to the trucks mileage and calculated the time taken based on the trucks time plus the distance * average miles per hour (which was 18).
- Since only 2 trucks could be out at a time, I decided that the best way to decide which trucks went out was to place all packages that were delayed and can only be on truck 2, on truck 2. This allowed for trucks 1 and 3 to go out right away and since truck 1 got back in time, truck 2 was able to go out relevatively early.
- The constraints on some of the packages were: can only be on truck 2, xyz packages must be delivered together, package 9 has the wrong address currently and wont be known until 10:20, and certain delivery times per package.

## What I learned
Doing this project, it taught me about implementing my own custom data structures which can then be modified and implemented into other structures. I also learned the nearest neighbor algorithm, along with others that I didn't use here, which gives me another tool to solve problems. The most enjoyable part of this project was coming up with different
methods to load the trucks while staying in the given constraints. Unfortunately I don't currently have time to implement an algorithm to sort the packages but I may go back to it in the future. The main thing that I learned was the ability to adapt and problem solve. This project required me to create and implement many new features
that I have not personally worked with before such as the hash table. 

![image](https://github.com/JMacPort/Package-Routing-Service/assets/145376972/5572d6b5-daff-4818-964a-175dfa809abb)
*Prompts on each run to display the number of miles the trucks took each and in total.*

![image](https://github.com/JMacPort/Package-Routing-Service/assets/145376972/3d4b6829-fb2f-4b0a-a605-b21004972bd9)
*With a given time and the package amount, all package status are shown. The user is then asked if they would like to run again.*

![image](https://github.com/JMacPort/Package-Routing-Service/assets/145376972/3c91a26f-66a6-44f3-a06d-9044a7ca6dcf)
*When the package amount of single is chosen, only that line is shown.*
