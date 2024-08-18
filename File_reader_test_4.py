import requests

# use github repo for directory
api_url = "https://api.github.com/repos/MarlingHeli/Manling_3DTP_91906_91907/contents/Waka Ama data/3.7B resource files"

ranking_dict = {}
refined_ranking = {}
folder_dict = {}


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
        # print("points: +0")
    else:
        # retrieve points based on place number and add to ranking_dict.
        # retrieves 1 point if place number is not in points_dict.
        ranking_dict[name] += points_dict.get(place, 1)
        # print(f"points: +{points_dict.get(place, 1)}")

        # print(f"{ranking_dict}\n")
        return ranking_dict


def file_reader(file_url):  # filters for place number and regional name
    response = requests.get(file_url)
    if response.status_code == 200:
        #print(response.text)
        contents = response.text.strip().split("\n")

        for record in contents[1:]:  # skip the first line
            #print(record)
            # split line into items at commas
            line = record.split(",")
            # check for empty place
            if line[0] == "":
                print(f"Error: place number missing. Ignoring line:\n{line}\n")
            # check for empty association name
            elif line[5] == "":
                print(f"Error: regional association missing. Ignoring line:\n{line}\n")
            else:
                points_calculator(line[0], line[5])

    else:
        print("Failed to get file contents :(")

def folder_reader(year_url):  # gets number of final files
    response = requests.get(year_url)
    # if successfully get url for year folder
    if response.status_code == 200:
        print("\nFolder found!")
        # get contents of year folder
        contents = response.json()
        # print("contents", contents)

        # count number of files
        print(f"number of files: {len(contents)}\n")

        final_files = {}
        for file in contents:
            # print("file", file)
            # filter for final files
            if "Final" in file["name"]:
                # get download url for each final file
                final_files[file["name"]] = file["download_url"]

        #print("final files", final_files)

        # download data from each final file
        for file in final_files:
            file_reader(final_files[file])

        refined_ranking = dict(sorted(ranking_dict.items(), key=lambda item: item[1], reverse=True))
        print("---\nRegional Association Points")
        for key, value in refined_ranking.items():
            print(f"{key}, {value}")
        return refined_ranking

    else:
        print("Failed to get folder contents :(")


def get_directory(url):  # get contents of 3.7B folder from github directory
    # send request to get api url
    response = requests.get(url)
    # 200 is the standard code for a successful http request sent by server
    if response.status_code == 200:
        # grab all the information about files in the 3.7B folder (as dictionaries in list)
        contents = response.json()
        # print(contents)

        # add folder name and url to dictionary
        for item in contents:
            # check if item is directory (folder)
            if item["type"] == "dir":
                folder_dict[item["name"]] = item["url"]

        print(f"Folders found: {', '.join(folder_dict.keys())}")
        # print(folder_dict)

        # select year folder
        year = int(input("\nSelect year (integer):\n"))
        folder = f"WakaNats{year}"

        if folder in folder_dict:
            # get url based on folder selected
            folder_url = folder_dict[folder]
            folder_reader(folder_url)
        else:
            print("Sorry! Folder not found :(")

    else:
        print("Failed to get directory contents :(")


get_directory(api_url)
