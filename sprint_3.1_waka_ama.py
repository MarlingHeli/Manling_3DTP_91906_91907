from tkinter import *
import requests
from concurrent.futures import ThreadPoolExecutor

# use github repo for directory
api_url = "https://api.github.com/repos/MarlingHeli/Manling_3DTP_91906_91907/contents/Waka Ama data/3.7B resource files"

ranking_dict = {}
folder_dict = {}


class Menu:
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
                Ranker()
            else:
                self.error_label.config(text="Sorry! Folder not found for the selected year.")
        else:
            self.error_label.config(text="Failed to get directory contents.")

    def year_check(self):

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


class Ranker:
    def __init__(self):
        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()

        # give buttons their own grid
        self.menu_buttons = Frame(bg="#FAFFFD")
        self.menu_buttons.grid()

        self.menu_heading = Label(self.frame,
                                  text="Ranking Calculator",
                                  font=("Arial", "22", "bold"), bg="#FAFFFD")
        self.menu_heading.grid(row=0, pady=(60, 10))


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
