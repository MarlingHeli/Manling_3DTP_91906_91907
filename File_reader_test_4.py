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
points = 0


def file_reader(year):
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

            for record in contents:
                lines = record.strip().split("\n") #split file into lines at line breaks
                #print("lines:", lines)
                for line in lines:
                    line = line.split(",") #split values in line at the commas
                    print("split at commas:", line)

                    if line[0] is not None: #check if there is a place number
                        try:
                            print(f"place, association: {int(line[0])}, {line[5]}\n")
                        except:
                            print(f"Error: value missing. Ignoring line:\n{line}\n") #runs if place number is not int

            print() # newline for readability


file_reader(year=int(input("Select year: 2017, 2018\n")))
