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
} #remember: any other place is 1 point. DNS/DQ/Disqualified = 0 points.

def ranking_finder(year):
    # check current directory
    os.chdir(directory)
    #cwd = os.getcwd()
    #print("current working directory:", cwd)

    path = "WakaNats" + str(year)
    #print("path:", path)
    # change directory
    os.chdir(path)
    cwd = os.getcwd()
    print("new working directory:", cwd)

    # count number of files
    dir = os.listdir()
    num_files = len(dir)
    print("number of files:", num_files)

    # filter for final files
    final_files = []
    for file in dir:
        if "Final" in file:
            final_files.append(file)
    #print(f"\nlist of final files:\n{final_files}\n")

    # read each final file
    for file in final_files:
        with open(file, "r") as contents:
            # skip first line
            #contents.readline()

            for line in contents:
                #group names together
                line = line.replace(" ", "-")
                #remove commas
                line = line.replace (",", " ").strip().split()

                if int(line[0]) > 100:
                    line = ["-"] + line
                    print("no place:", line)

                elif len(line[1]) <5:
                    line = line[0] + ["-"] + line[1:]
                    print("no team id:", line)

                else:
                    print(line)
            print()


ranking_finder(year=int(input("Select year: 2017, 2018\n")))
