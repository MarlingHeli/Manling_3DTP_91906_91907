from tkinter import *
import requests
from concurrent.futures import ThreadPoolExecutor

# use github repo for directory
api_url = "https://api.github.com/repos/MarlingHeli/Manling_3DTP_91906_91907/contents/Waka Ama data/3.7B resource files"

ranking_dict = {}
folder_dict = {}


class Menu: # menu screen that also error checks input
    def __init__(self):
        # paragraph and button font
        font = ("Arial", "11")

        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()

        # give buttons their own grid
        self.menu_buttons = Frame(bg="#FAFFFD")
        self.menu_buttons.grid()

        self.menu_heading = Label(self.frame,
                                  text="Waka Ama ranking finder",
                                  font=("Arial", "22", "bold"), bg="#FAFFFD")
        self.menu_heading.grid(row=0, pady=(60, 10))
        # add description
        self.menu_description = Label(self.frame,
                                      text="Welcome to the unofficial Waka Ama ranking finder! "
                                           "Use this program to check the results of a "
                                           "previous competition by year.",
                                      font=("Arial", "12"),
                                      wrap=530, width=80, justify="left", bg="#FAFFFD")
        self.menu_description.grid(row=1)

        # add entry field for years
        self.year_var = StringVar()
        self.year_var.set("")
        self.year_label = Label(self.menu_buttons, text="Enter year:", font=("Arial", "12"), bg="#FAFFFD")
        self.year_entry = Entry(self.menu_buttons, textvariable=self.year_var, font=("Arial", "20"),
                                width=5, bg="#FAFFFD", highlightbackground="#000000", highlightthickness=1)
        self.year_label.grid(row=1, column=1, pady=(230, 10))
        self.year_entry.grid(row=1, column=2, pady=(230, 10))

        # give buttons a consistent black border
        self.button_find_border = Frame(self.menu_buttons, highlightbackground="#000000",
                                        highlightthickness=1, bd=1)
        self.button_find_border.grid(row=1, column=3, pady=(230, 10))

        self.button_help_border = Frame(self.menu_buttons, highlightbackground="#000000",
                                        highlightthickness=1, bd=1)
        self.button_help_border.grid(row=1, column=4, pady=(230, 10), padx=50)

        # create buttons
        self.button_find = Button(self.button_find_border, text="Find",
                                  font=font, bg="#C9FFDB", bd=0, highlightthickness=5,
                                  command=self.year_check)
        self.button_find.grid(row=2, column=3)

        self.button_help = Button(self.button_help_border, text="Help/information",
                                  font=font, bg="#DAFFC7", bd=0, highlightthickness=5,
                                  )
        self.button_help.grid(row=2, column=4)

        # give error message their own frame
        self.error_frame = Frame()
        self.error_frame.grid()
        self.error_label = Label(self.error_frame, text="", font=font, fg="red", bg="#FAFFFD")
        self.error_label.grid(row=1)

    def get_directory(self, url, year):  # get contents of 3.7B folder from github directory
        # send request to get api url
        response = requests.get(url)
        # 200 is the standard code for a successful http request sent by server
        if response.status_code == 200:
            # grab all the information about files in the 3.7B folder (as dictionaries in list)
            contents = response.json()

            # add folder name and url to dictionary
            for item in contents:
                # check if item is directory (folder)
                if item["type"] == "dir":
                    folder_dict[item["name"]] = item["url"]

            folder = f"WakaNats{year}"

            if folder in folder_dict:
                folder_url = folder_dict[folder]
                # hide menu elements for ranking calculator screen
                self.menu_buttons.destroy()
                self.menu_description.destroy()
                self.menu_heading.destroy()
                Ranker(folder_url)
            else:
                self.error_label.config(text="Sorry! Folder not found for the selected year.")
        else:
            self.error_label.config(text=f"Failed to get directory contents. Status code: {response}")

    def year_check(self): # error check year input

        try:
            year_input = self.year_var.get()
            year = int(year_input)
            # set boundaries for year input
            if 2017 <= year <= 2030:
                # clear any previous error messages
                self.error_label.config(text="")
                self.get_directory(api_url, year)
            else:
                self.error_label.config(text="Please enter a year between 2017 and 2030.")
        except ValueError:
            self.error_label.config(text="Please enter a whole number.")


class Ranker: # ranking calculator screen that calculates points
    def __init__(self, folder_url):
        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()

        # give buttons their own grid
        self.menu_buttons = Frame(bg="#FAFFFD")
        self.menu_buttons.grid()

        self.menu_heading = Label(self.frame,
                                  text="Ranking Calculator",
                                  font=("Arial", "22", "bold"), bg="#FAFFFD")
        self.menu_heading.grid(row=0, pady=(60, 10))
        self.folder_reader(folder_url)

    def points_calculator(self, place, name):  # assign points based on place number
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
        if self.name not in ranking_dict:
            ranking_dict[name] = 0

        # give 0 points to disqualified teams
        if place == "DNS" or place == "DQ" or place == "Disqualified":
            ranking_dict[name] += 0
            # print("points: +0")
        else:
            # retrieve points based on place number and add to ranking_dict.
            # retrieves 1 point if place number is not in points_dict.
            ranking_dict[name] += points_dict.get(place, 1)

            return ranking_dict

    def file_reader(self, file_url):  # filters for place number and regional name
        response = requests.get(file_url)
        if response.status_code == 200:
            contents = response.text.strip().split("\n")
            # skip the first line
            for record in contents[1:]:
                # split line into items at commas
                line = record.split(",")
                # check for empty place
                if line[0] == "":
                    print(f"Error: place number missing. Ignoring line:\n{line}\n")
                # check for empty association name
                elif line[5] == "":
                    print(f"Error: regional association missing. Ignoring line:\n{line}\n")
                else:
                    self.points_calculator(line[0], line[5])

        else:
            print("Failed to get file contents :(")

    def folder_reader(self, year_url):  # filters for and gets number of final files
        response = requests.get(year_url)
        # if successfully get url for year folder
        if response.status_code == 200:
            print("\nFolder found!")
            # get contents of year folder
            contents = response.json()
            # count number of files
            print(f"number of files: {len(contents)}\n")

            final_files = []
            for file in contents:
                # filter for final files
                if "Final" in file["name"]:
                    # get download url for each final file
                    final_files.append(file["download_url"])

            # speed up reading
            with ThreadPoolExecutor(max_workers=3) as executor:
                # start 3 parallel processes using file_reader function and final files dict
                executor.map(self.file_reader, final_files)

            # print ranking results
            refined_ranking = dict(sorted(ranking_dict.items(), key=lambda item: item[1], reverse=True))
            print("---\nRegional Association Points")
            for key, value in refined_ranking.items():
                print(f"{key}, {value}")
            # return refined_ranking

        else:
            print("Failed to get folder contents :(")


class Info:
    def __init__(self):
        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()

        # give buttons their own grid
        self.menu_buttons = Frame(bg="#FAFFFD")
        self.menu_buttons.grid()

        self.menu_heading = Label(self.frame,
                                  text="Help/Information",
                                  font=("Arial", "22", "bold"), bg="#FAFFFD")
        self.menu_heading.grid(row=0, pady=(60, 10))


# keep window on screen
if __name__ == "__main__":
    window = Tk()
    window.title("Waka Ama ranking finder")
    window.geometry("700x500")
    window.configure(bg="#FAFFFD")
    Menu()
    window.mainloop()
