import os

ranking_dict = {}
refined_ranking = {}

def points_calculator(place, name):  # assign points based on place number
    points_dict = {
        "1": 8,
        "2": 7,
        "3": 6,
        "4": 5,
        "5": 4,
        "6": 3,
        "7": 2,
        "8": 1,
    }
    # initialise keys and values
    if name not in ranking_dict:
        ranking_dict[name] = 0

    # give 0 points to disqualified teams
    if place == "DNS" or place == "DQ" or place == "Disqualified":
        ranking_dict[name] += 0
        #print("points: +0")
    else:
        # retrieve points based on place number and add to ranking_dict.
        # retrieves 1 point if place number is not in points_dict.
        ranking_dict[name] += points_dict.get(place, 1)
        #print(f"points: +{points_dict.get(place, 1)}")

        #print(f"{ranking_dict}\n")
        return ranking_dict


def file_reader(year):  # gets number of final files and filters for place number and regional name
    # set current directory
    os.chdir(directory)

    path = f"WakaNats{year}"
    # change directory
    os.chdir(path)
    cwd = os.getcwd()
    print("new working directory:", cwd)

    # count number of files
    new_directory = os.listdir()
    num_files = len(new_directory)
    print(f"number of final files:{num_files}\n")

    # filter for final files
    final_files = []
    for file in new_directory:
        if "Final" in file:
            final_files.append(file)

    # read each final file
    for file in final_files:
        with open(file, "r") as contents:
            # skip first line
            contents.readline()

            for record in contents:
                # split file into lines at line breaks
                lines = record.strip().split("\n")
                for line in lines:
                    # split values in line at the commas
                    line = line.split(",")
                    #print(line)

                    # error if place number is empty string
                    if line[0] == "":
                        print(f"Error: place number missing. Ignoring line:\n{line}\n")
                    elif line[5] == "":
                        print(f"Error: regional association missing. Ignoring line:\n{line}\n")
                    else:
                        #print(f"place, association: {line[0]}, {line[5]}")
                        # calculate points
                        points_calculator(line[0], line[5])

    # sort dict in descending order
    refined_ranking = dict(sorted(ranking_dict.items(),
                                  key=lambda item: item[1], reverse=True))

    #print(f"\n{refined_ranking}")
    print("---\nRegional Association Points")
    for key, value in refined_ranking.items():
        print(f"{key}, {value}")
    return refined_ranking


directory = input("Please enter your directory for 3.7B resource files, or press enter to use the default directory:"
                  "\nC:/Users/hmarl/OneDrive/Documents/DTP3/Programming/Assessment/Waka Ama data/3.7B resource files\n")

default_dir = "C:/Users/hmarl/OneDrive/Documents/DTP3/Programming/Assessment/Waka Ama data/3.7B resource files"

#use default directory if user presses enter
if directory == "":
    directory = default_dir

file_reader(year=int(input("\nSelect year: 2017, 2018\n")))

