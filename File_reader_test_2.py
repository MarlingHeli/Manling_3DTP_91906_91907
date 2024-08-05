import os

directory = ("C:/Users/hmarl/OneDrive/Documents/DTP3/Programming/Assessment/Waka Ama data/3.7B resource files")

points_dict = {
    "1": 8,
    "2": 7,
    "3": 6,
    "4": 5,
    "5": 4,
    "6": 3,
    "7": 2,
    "8": 1,
    "DNS": 0,
    "DQ": 0,
    "Disqualified": 0,
    "None": 0,
}  # remember: any other place is 1 point. DNS/DQ/Disqualified = 0 points.

ranking_dict = {}
def ranking_finder(year):
    # check current directory
    os.chdir(directory)
    # cwd = os.getcwd()
    # print("current working directory:", cwd)

    path = "WakaNats" + str(year)
    # print("path:", path)
    # change directory
    os.chdir(path)
    cwd = os.getcwd()
    print("new working directory:", cwd)

    # count number of files
    new_directory = os.listdir()
    num_files = len(new_directory)
    print("number of files:", num_files)

    # filter for final files
    final_files = []
    for file in new_directory:
        if "Final" in file:
            final_files.append(file)
    # print(f"\nlist of final files:\n{final_files}\n")

    # read each final file
    for file in final_files:
        with open(file, "r") as contents:
            # skip first line
            contents.readline()
            contents.readline()

            for line in contents:
                # group names together
                line = line.replace(" ", "-")
                # remove commas
                line = line.replace(",", " ").strip().split()

                #####################################################################################################
                # Look for missing items in the line
                if len(line) >= 10:
                    print(line)

                else: 
                    while len(line) < 10:

                        # check if there is place number
                        if not line[0].isdigit() or len(line[0]) >= 5: #if index 0 is not a number or is more than/or 5 characters
                            line.insert(0, "None")
                            print("no place:")
    
                        # check if there is team id
                        if not line[1].isdigit() or len(line[1]) <=4: #if index 1 is not a number or is less than/or 4 characters
                            line.insert(1, "None")
                            print("no team id:")
    
                        # check if there is lane number
                        if not line[2].isdigit(): #if index 2 is not a number
                            line.insert(2, "None")
                            print("no lane number:")
    
                        # check if there is team name
                        if any(chr.isdigit() for chr in line[4]) and not line[3].isdigit(): #if index 4 has numbers and index 3 is string
                            line.insert(3, "None")
                            print("no team name:")
    
                        # check if there is regional name
                        if any(chr.isdigit() for chr in line[4]): #if any number in index 4
                            line.insert(4, "None")
                            print("no regional name:")

                        print(line)
                        break

            print()

ranking_finder(year=int(input("Select year: 2017, 2018\n")))
