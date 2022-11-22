""" 
    THIS IS UNUSED - DON'T BOTHER USING IT
    I'm just keeping it here if any dev has the curiosity to see how it works or how it was done.

    ###########################################################################################################################################

    Author: VIRUXE
    GitHub: https://gist.github.com/VIRUXE/9c56435627604338ad9c8a506648f7a8

    This script compiles all the vehicles in the cwd onto a json file. To be used with my resource, that installs the vehicles into the game.

    It will create a file called vehicles.json in the cwd (if it's not created already),
    which will contain all the vehicles in the cwd, by their brands and models.

    Folder format: brand-model(_name) - Can have multiple underscores, but only one dash, to separate the brand and model.
"""

import os
import json
import sys

class Color:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Check if command line argument "fresh" is passed in order to start with a fresh vehicles.json file or just create the file if it doesn't exist
# You would want to start fresh if vehicles.json has vehicles that you don't want anymore
# This way the resource will not add those vehicle's info to the game for no reason
if (len(sys.argv) > 1 and sys.argv[1] == "fresh") or not os.path.exists("vehicles.json"):
    with open("vehicles.json", "w") as f:
        f.write("{}")

brands_compiled = 0
vehicles_compiled = 0

# Get all folders that contain a dash in the name
folders = [f for f in os.listdir('.') if os.path.isdir(f) and '-' in f]

# Split the folder name into two parts using a dash as the delimiter
# The first part is the vehicle brand
# The second part is the vehicle description
# Replace the underscore in the description with a space
vehicles = {}
for folder in folders:
    print(Color.HEADER + 'Processing folder: ' + Color.BOLD + folder + Color.ENDC)
    brand, description = folder.split('-', -1)
    # Only replace if there is an underscore in the description
    if '_' in description:
        description = description.replace('_', ' ')

    # Capitalize the first letter of the brand and all words in description
    brand = brand.capitalize()
    description = description.title()

    print(Color.OKCYAN + '-> Brand: ' + Color.BOLD + brand + Color.ENDC)
    print(Color.OKCYAN + '-> Generated Description: ' + Color.BOLD + description + Color.ENDC)

    vehicles[folder] = {
        'brand': brand,
        'description': description
    }

# Go into the folder and get the vehicles.meta file
# Open the vehicles.meta file as XML and get the modelName field
# Use modelName as a key in the dictionary and the brand and description as the value
for folder in folders:
    if os.path.isfile(folder + '/vehicles.meta'):
        with open(f'{folder}/vehicles.meta', 'r') as f:
            found = False

            # Read the file line by line and look for the modelName field in the XML document
            for line in f:
                if 'modelName' in line: # modelName field found
                    model_name = line.split('>', 1)[1].split('<', 1)[0] # Get the modelName value
                    #  Only do something if there is a modelName field
                    if model_name:
                        print(Color.WARNING + '-> Model Name: ' + Color.BOLD + model_name + Color.ENDC)
                        vehicles[model_name] = vehicles[folder]
                        del vehicles[folder]
                        found = True
                        break # modelName field found, no need to continue reading the file
            
            # Delete the folder from the dictionary if modelName is not found
            if found == False:
                del vehicles[folder]
                print(Color.FAIL + '* Error: Did not find "modelName" field in "vehicles.meta"' + Color.ENDC)
    # Delete the folder from the dictionary if vehicles.meta is not found
    else:
        del vehicles[folder]
        print(Color.FAIL + '* Error: Did not find "vehicles.meta"' + Color.ENDC)

# Compare the vehicles dictionary to the vehicles.json file using the brand as the key and the modelName and description as values
# If the modelName is not in the vehicles.json file, add it
# modelName is the first part of the value
# description is the second part of the value
with open('vehicles.json', 'r') as f:
    vehicles_json = json.load(f)

print(Color.HEADER + '\nFinished gathering info. Comparing "vehicles.json" to vehicles dictionary...' + Color.ENDC)
print(Color.BOLD + '---------------------------' + Color.ENDC)
# Loop through the vehicles dictionary
for modelName, modelData in vehicles.items():
    print(f"Comparing {Color.BOLD}{modelData['brand']} - {modelData['description']}") # Well this looks ugly, but not as ugly as the alternative

    brand = modelData['brand'].lower()

    # If modelData['brand'] is not in vehicles.json, add the brand and push modelData onto the array
    if brand not in vehicles_json:
        vehicles_json[brand] = []
        vehicles_json[brand].append([modelName, modelData['description']])
        brands_compiled += 1
        vehicles_compiled += 1
        print(Color.OKGREEN + '-> Added brand: ' + Color.BOLD + modelData['brand'] + Color.ENDC) # Print it capitalized to look nice
    # If brand is in vehicles.json, check if the modelName is in the array
    else:
        found = False
        print(Color.OKBLUE + '-> Found brand: ' + Color.BOLD + brand.capitalize() + Color.ENDC) # Print it capitalized to look nice

        # Loop through the array and check if the modelName is in the array, if not add modelName and description as values
        for i in range(len(vehicles_json[brand])):
            if modelName in vehicles_json[brand][i]:
                found = True
                print(Color.WARNING + '-> Not adding ' + Color.BOLD + modelName + Color.ENDC + Color.WARNING + ' as it already exists.' + Color.ENDC)
                print('Would you like to update the description? (y/n)')
                user_input = input()
                if user_input == "y":
                    print(Color.OKGREEN + "Please enter the description: " + Color.ENDC)
                    new_description = input()
                    # Check if the input is valid
                    if len(new_description) > 1:
                        vehicles_json[brand][i][1] = new_description
                        print(Color.OKGREEN + "Description changed to: " + Color.BOLD + new_description + Color.ENDC)
                break # modelName found, no need to continue looping

        if found == False: # Model wasn't found in the array so let's add it
            # Ask for user input to see if he wants the generated description or not
            print(Color.OKGREEN + "Would you like to provide a different Description? (y/n)" + Color.ENDC) # Why is this not using the Color class?
            user_input = input()
            if user_input == "y":
                print(Color.OKGREEN + Color.BOLD + "Please enter the description: " + Color.ENDC)
                new_description = input() # Get the new description from the user
                # Check if the input is valid
                # Account for interruping the program
                if new_description == "" or len(new_description) < 1 or new_description == "exit": 
                    print(Color.WARNING + "Invalid description. Using the generated one." + Color.ENDC)
                else:
                    modelData['description'] = new_description.title() # Capitalize the first letter of the new description
                    print(Color.OKGREEN + "Description changed to: " + Color.BOLD + new_description.title() + Color.ENDC)
            else:
                print(Color.OKGREEN + "Using the Generated one it is." + Color.ENDC)

            # Add the modelName and description to the array
            vehicles_json[brand].append([modelName, modelData['description']])
            vehicles_compiled += 1
            print(Color.OKGREEN + '-> Added model: ' + Color.BOLD + modelName + Color.ENDC)

print(Color.BOLD + '\nCompiled ' + str(brands_compiled) + ' brands and ' + str(vehicles_compiled) + ' vehicles' + Color.ENDC)

# Write the vehicles_json dictionary to the vehicles.json file
with open('vehicles.json', 'w') as f:
    print('Writing vehicles.json')
    json.dump(vehicles_json, f, indent=4, sort_keys=True) # Dump the vehicles_json dictionary to the vehicles.json file
    print('Wrote vehicles.json file')