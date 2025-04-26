import os
import time

landmarks = ["CC", "ISC"]
while True:
    print("____________________________________________________________________________________________________________")
    print("Locations:")
    for i in landmarks:
        print(i)
    print("____________________________________________________________________________________________________________")
    starting_point = input("Select a starting point from the options above: ")
    if starting_point.upper() in landmarks:
        break
    else:
        print("Location not found, please try again")
time.sleep(1)
print("\n" * 80)
while True:
    print("____________________________________________________________________________________________________________")
    print("Locations:")
    for i in landmarks:
        print(i)
    print("____________________________________________________________________________________________________________")
    destination = input(f"Select a destination to get to from {starting_point} from the options above: ")
    if destination.upper() in landmarks:
        break
    else:
        print("Location not found, please try again")

print(starting_point, destination)




