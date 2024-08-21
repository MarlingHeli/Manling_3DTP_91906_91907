from tkinter import *
import requests
from concurrent.futures import ThreadPoolExecutor

# use GitHub repo for directory
api_url = "https://api.github.com/repos/MarlingHeli/Manling_3DTP_91906_91907/contents/Waka Ama data/3.7B resource files"

ranking_dict = {}
folder_dict = {}

# paragraph and button font
font = ("Arial", "12")
# background colour
bg = "#FAFFFD"


#######################################################################################################################
class Menu:  # menu screen that also error checks input
    def __init__(self):
        self.frame = Frame(bg=bg)
        self.frame.grid()

        # give buttons their own grid
        self.menu_buttons = Frame(bg=bg)
        self.menu_buttons.grid()

        self.menu_heading = Label(self.frame,
                                  text="Waka Ama ranking finder",
                                  font=("Arial", "22", "bold"), bg=bg)
        self.menu_heading.grid(row=0, pady=(60, 10))
        # add description
        self.menu_description = Label(self.frame,
                                      text="Welcome to the unofficial Waka Ama ranking finder! "
                                           "Use this program to check the results of a "
                                           "previous competition by year.",
                                      font=("Arial", "12"),
                                      wrap=530, width=80, justify="left", bg=bg)
        self.menu_description.grid(row=1)

        # add entry field for years
        self.year_var = StringVar()
        self.year_var.set("")
        self.year_label = Label(self.menu_buttons, text="Enter year:", font=("Arial", "12"), bg=bg)
        self.year_entry = Entry(self.menu_buttons, textvariable=self.year_var, font=("Arial", "20"),
                                width=5, bg=bg, highlightbackground="#000000", highlightthickness=1)
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
                                  command=Info)
        self.button_help.grid(row=2, column=4)

        # give error message their own frame
        self.error_frame = Frame()
        self.error_frame.grid()
        self.error_label = Label(self.error_frame, text="", font=font, fg="red", bg=bg)
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
                Ranker(folder_url, year)
                # hide menu elements for ranking calculator screen
                self.menu_buttons.destroy()
                self.frame.destroy()
                self.error_frame.destroy()
            else:
                self.error_label.config(text="Sorry! Folder not found for the selected year.")
        else:
            self.error_label.config(text=f"Failed to get directory contents. Status code: {response}")

    def year_check(self):  # error check year input
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


#######################################################################################################################
class Ranker:  # ranking calculator screen that calculates points
    def __init__(self, folder_url, year):
        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()

        self.ranker_heading = Label(self.frame,
                                    text=f"Ranking Calculator - {year}",
                                    font=("Arial", "22", "bold"), bg=bg)
        self.ranker_heading.grid(row=0, pady=(35, 5))

        self.ranker_description = Label(self.frame,
                                        text="Below is a preview of the rankings. To download the file "
                                             "as a .csv file, click 'Export to csv'.",
                                        font=("Arial", "12"),
                                        wrap=530, width=80, justify="left", bg=bg)
        self.ranker_description.grid(row=1, pady=(5, 3))

        self.window_frame = Frame()
        self.window_frame.grid()

        # create scroll bar
        self.scrollbar = Scrollbar(self.window_frame)
        self.scrollbar.grid(row=1, column=2)

        # create results list
        self.results = Listbox(self.window_frame, bg="white", width=60, height=10,
                               font=font, yscrollcommand=self.scrollbar.set)

        # give buttons their own grid
        self.ranker_buttons = Frame(bg=bg)
        self.ranker_buttons.grid(pady=(30, 10))

        # give buttons a consistent black border
        self.button_csv_border = Frame(self.ranker_buttons, highlightbackground="#000000",
                                       highlightthickness=1, bd=1)
        self.button_csv_border.grid(row=1, column=1, padx=50)

        self.button_return_border = Frame(self.ranker_buttons, highlightbackground="#000000",
                                          highlightthickness=1, bd=1)
        self.button_return_border.grid(row=1, column=2, padx=50)

        # create buttons
        self.button_csv = Button(self.button_csv_border, text="Export to csv",
                                 font=font, bg="#BAFFD3", bd=0, highlightthickness=5,
                                 )
        self.button_csv.grid(row=1, column=1)
        # return to menu
        self.button_return = Button(self.button_return_border, text="Return",
                                    font=font, bg="#C9FFDB", bd=0, highlightthickness=5,
                                    command=lambda: [self.frame.destroy(), self.window_frame.destroy(),
                                                     self.ranker_buttons.destroy(), Menu()])
        self.button_return.grid(row=1, column=2)

        self.error_frame = Frame(bg=bg)
        self.error_frame.grid()

        # add error label
        self.error_label = Label(self.window_frame, text="error", font=font, fg="red")
        self.error_label.grid(row=1)

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
                if line[0] != "" and line[5] != "":
                    self.points_calculator(line[0], line[5])
        else:
            self.error_label.config(text="Failed to get file contents :(")

    def folder_reader(self, year_url):  # filters for and gets number of final files
        response = requests.get(year_url)
        # if successfully get url for year folder
        if response.status_code == 200:
            # print("\nFolder found!")
            # get contents of year folder
            contents = response.json()

            # count number of files
            label_files = Label(self.frame, text=f"Number of files: {len(contents)}", font=font,
                                bg=bg)
            label_files.grid(row=2)

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

            # print ranking results in descending order
            refined_ranking = dict(sorted(ranking_dict.items(), key=lambda item: item[1], reverse=True))
            self.results.insert(0, "Regional Association Points")
            index = 1
            for key, value in refined_ranking.items():
                self.results.insert(index, f"{index} - {key}, {value}")
                index += 1

            # display results list
            self.results.grid(row=1, column=1)
            self.scrollbar.config(command=self.results.yview)

        else:
            self.error_label.config(text="Failed to get folder contents :(")


#######################################################################################################################
class Info:
    def __init__(self):
        self.frame = Frame(bg=bg)
        self.frame.grid()

        # give buttons their own grid
        self.info_buttons = Frame(bg=bg)
        self.info_buttons.grid()

        self.info_heading = Label(self.frame,
                                  text="Help/Information",
                                  font=("Arial", "22", "bold"), bg=bg)
        self.info_heading.grid(row=0, pady=(60, 10))


#######################################################################################################################
# keep window on screen
if __name__ == "__main__":
    window = Tk()
    window.title("Waka Ama ranking finder")
    window.geometry("700x500")
    window.configure(bg=bg)
    Menu()
    window.mainloop()
