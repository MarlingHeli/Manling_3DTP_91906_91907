import tkinter
import tkinter.messagebox
from tkinter import *
import requests
from concurrent.futures import ThreadPoolExecutor
from tkinter import filedialog
from pathlib import Path
import webbrowser

# use GitHub repo for directory
api_url = "https://api.github.com/repos/MarlingHeli/Manling_3DTP_91906_91907/contents/Waka Ama data/3.7B resource files"

ranking_dict = {}
folder_dict = {}

# paragraph and button font
font = ("Arial", "12")
# background colour
bg = "#FAFFFD"


#######################################################################################################################
# menu screen that also error checks input
class Menu:
    def __init__(self):
        # create frames
        self.frame = Frame(bg=bg)
        self.frame.grid()
        self.button_frame = Frame(bg=bg)
        self.button_frame.grid()
        self.error_frame = Frame()
        self.error_frame.grid()

        # add text
        self.menu_heading = Label(self.frame, text="Waka Ama ranking finder", font=("Arial", "22", "bold"), bg=bg)
        self.menu_heading.grid(row=0, pady=(60, 10))

        self.menu_desc = Label(self.frame,
                               text="Welcome to the unofficial Waka Ama ranking finder! Use this program to "
                                    "check the results of a previous competition by year.", font=("Arial", "12"),
                               wrap=530, width=80, justify="left", bg=bg)
        self.menu_desc.grid(row=1)

        # add entry field for years
        self.year_var = StringVar()
        self.year_var.set("")
        self.year_label = Label(self.button_frame, text="Enter year:", font=("Arial", "12"), bg=bg)
        self.year_entry = Entry(self.button_frame, textvariable=self.year_var, font=("Arial", "20"),
                                width=5, bg=bg, highlightbackground="#000000", highlightthickness=1)
        self.year_label.grid(row=1, column=1, pady=(230, 10))
        self.year_entry.grid(row=1, column=2, pady=(230, 10))

        # give buttons a consistent black border
        self.find_border = Frame(self.button_frame, highlightbackground="#000000", highlightthickness=1, bd=1)
        self.find_border.grid(row=1, column=3, pady=(230, 10))

        self.help_border = Frame(self.button_frame, highlightbackground="#000000", highlightthickness=1, bd=1)
        self.help_border.grid(row=1, column=4, pady=(230, 10), padx=50)

        # create buttons
        self.button_find = Button(self.find_border, text="Find", font=font, bg="#C9FFDB", bd=0, highlightthickness=5,
                                  command=self.year_check)
        self.button_find.grid(row=2, column=3)

        self.button_help = Button(self.help_border, text="Help/information", font=font, bg="#DAFFC7", bd=0,
                                  highlightthickness=5,
                                  command=lambda: [self.frame.destroy(), self.button_frame.destroy(),
                                                   self.error_frame.destroy(), Info()])
        self.button_help.grid(row=2, column=4)

        # add error label
        self.error_label = Label(self.error_frame, text="", font=font, fg="red", bg=bg)
        self.error_label.grid(row=1)

        # add loading label
        self.loading_label = Label(self.error_frame, text="Loading...", font=font, bg=bg)

    # get contents of 3.7B folder from GitHub directory
    def get_directory(self, url, year):
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
                self.loading_label.grid(row=1)
                self.frame.update()
                folder_url = folder_dict[folder]
                # hide menu elements for ranking calculator screen
                self.button_frame.destroy()
                self.frame.destroy()
                self.error_frame.destroy()
                # run Ranker class
                Ranker(folder_url, year)
            else:
                self.error_label.config(text="Sorry! Folder not found for the selected year.")
        else:
            self.error_label.config(text=f"Failed to get directory contents. Status code: {response}")

    # error check year input
    def year_check(self):
        try:
            year_input = self.year_var.get()
            year = int(year_input)
            # set boundaries for year input
            if 2017 <= year <= 2030:
                # clear any previous error messages
                self.error_label.config(text="")
                # run get_directory method
                self.get_directory(api_url, year)
            else:
                self.error_label.config(text="Please enter a year between 2017 and 2030.")
        except ValueError:
            self.error_label.config(text="Please enter a whole number.")


#######################################################################################################################
# ranking calculator screen that calculates points
class Ranker:
    def __init__(self, folder_url, year):
        # create frames
        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()
        # canvas is better for scrolling elements
        self.window_canvas = Canvas(self.frame)
        self.window_canvas.grid(row=3)
        self.button_frame = Frame(bg=bg)
        self.button_frame.grid(pady=(25, 10))
        self.error_frame = Frame(bg=bg)
        self.error_frame.grid()

        # add text
        self.ranker_heading = Label(self.frame, text=f"Ranking Calculator - {year}", font=("Arial", "22", "bold"),
                                    bg=bg)
        self.ranker_heading.grid(row=0, pady=(35, 0))

        self.ranker_desc = Label(self.frame,
                                 text="Below is a preview of the rankings. To download the file as a .csv file,"
                                      " click 'Export to csv'.", font=("Arial", "12"), wrap=530, width=80,
                                 justify="left", bg=bg)
        self.ranker_desc.grid(row=1, pady=5)

        # create scroll bar
        self.scrollbar = Scrollbar(self.window_canvas)
        self.scrollbar.grid(row=3, column=2, sticky="nsew")

        # create results list
        self.results = Listbox(self.window_canvas, bg="white", width=60, height=12, font=font,
                               yscrollcommand=self.scrollbar.set)

        # give buttons a consistent black border
        self.csv_border = Frame(self.button_frame, highlightbackground="#000000", highlightthickness=1, bd=1)
        self.csv_border.grid(row=1, column=1, padx=50)

        self.return_border = Frame(self.button_frame, highlightbackground="#000000", highlightthickness=1, bd=1)
        self.return_border.grid(row=1, column=2, padx=50)

        # create buttons
        self.button_csv = Button(self.csv_border, text="Export to csv", font=font, bg="#BAFFD3", bd=0,
                                 highlightthickness=5, command=lambda: self.export_csv(year))
        self.button_csv.grid(row=1, column=1)
        # return to menu
        self.button_return = Button(self.return_border, text="Return",
                                    font=font, bg="#C9FFDB", bd=0, highlightthickness=5,
                                    command=lambda: [self.frame.destroy(), self.window_canvas.destroy(),
                                                     self.button_frame.destroy(), self.error_frame.destroy(), Menu()])
        self.button_return.grid(row=1, column=2)

        # add error label
        self.error_label = Label(self.error_frame, text="", font=font, fg="red", bg=bg)
        self.error_label.grid(row=0)

        # run folder_reader method
        self.folder_reader(folder_url)

    # assign points based on place number
    def points_calculator(self, place, name):
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

    # filters for place number and regional name
    def file_reader(self, file_url):
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

    # organise ranking dictionary and display it
    def ranking_results(self):
        # print ranking results in descending order
        refined_ranking = dict(sorted(ranking_dict.items(), key=lambda item: item[1], reverse=True))
        self.results.insert(0, "Place, Association, Points")
        index = 1
        for key, value in refined_ranking.items():
            self.results.insert(index, f"{index}, {key}, {value}")
            index += 1

        # display results list
        self.results.grid(row=3, column=1)
        self.scrollbar.config(command=self.results.yview)

    # filters for and gets number of final files
    def folder_reader(self, year_url):
        response = requests.get(year_url)
        # if response successfully gets url for year folder
        if response.status_code == 200:
            # get contents of year folder
            contents = response.json()

            # count number of files
            label_files = Label(self.frame, text=f"Number of files: {len(contents)}", font=font, bg=bg)
            label_files.grid(row=2, pady=(3, 15))

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
            self.ranking_results()

        else:
            self.error_label.config(text="Failed to get folder contents :(")

    # download results as csv file
    def export_csv(self, year):
        try:
            # get user's download path
            downloads = str(Path.home() / "Downloads")
            csv = filedialog.asksaveasfile(initialdir=downloads, filetypes=[("csv file", "*.csv")], mode="w",
                                           initialfile=f"WakaAmaRanking{year}.csv")

            # check if user presses cancel (returning empty value/None)
            if csv is None:
                return

            # put listbox contents in csv file
            csv.write("\n".join(self.results.get(0, END)))
            csv.close()

        # ask users to close the file if it is open
        except PermissionError:
            tkinter.messagebox.showerror(title="Override issue", message="Please close the original file before "
                                                                         "overriding it.")


#######################################################################################################################
class Info:
    def __init__(self):
        # create frames
        self.frame = Frame(bg=bg, padx=50)
        self.frame.grid()
        self.button_frame = Frame(bg=bg)
        self.button_frame.grid()

        # add text
        self.info_heading = Label(self.frame, text="Help/Information", font=("Arial", "22", "bold"), bg=bg)
        self.info_heading.grid(row=0, pady=(40, 15))

        info_1 = "This program reads Waka Ama's competition data, calculates the total points earned by each " \
                 "association, and ranks them. Since this program sources the data from GitHub (online), factors " \
                 "like the network, data size, server response time, etc., can influence how quickly the program " \
                 "processes files.\n\n" \
                 "How to use the program:\nAt the Menu screen, type in the year that you want " \
                 "the program to analyse. The earliest year is 2017 and latest year is 2030. The program will check " \
                 "whether that year exists as a folder, then produces the results. You will have the option to " \
                 "download the results as a .csv file. The .csv file downloaded will be named WakaAmaRanking{year}," \
                 " where {year} is the year that you selected." \
                 "\n\nAdding your own data:\nTo add your year folder," \
                 " go to this repository on GitHub:\n" \

        info_2 = "\nYou will have to fork the repository. If your folder has over 100 files, GitHub online " \
                 "will not be able to process it from its size. You could try uploading the files in batches. " \
                 "Otherwise, you will have to download GitHub desktop and possibly Git Large File Storage.\n\n" \
                 "Rules:\nPlease name your year folder 'WakaNats{year}' (without quotations and curly brackets), " \
                 "where year is the year of your folder. Example: WakaNats2019. If you do not follow this format, " \
                 "the program will not detect your folder. Similarly, files of the final games must have 'Final'" \
                 " in its title or else the program will not find it. Please do not store folders inside the " \
                 "year folder. Make sure your year folder is unzipped." \
                 "\n\nFork using GitHub desktop:\n1. On GitHub online, go to the repository linked " \
                 "above.\n2. In the top right, click the fork button.\n3. Name and copy the link of your forked" \
                 " repository.\n4. Go to GitHub Desktop.\n5. Go to 'File'." \
                 "\n6. Click 'Clone Repository.'\n7. At URL, paste in your forked GitHub link.\n8. Pick where to " \
                 "save your repository.\n9.GitHub will ask you to contribute to the original" \
                 " repository or your own.\n    Pick your own repository if you do not want to affect the original." \
                 "\n10. Open your local repository folder (Ctrl + Shift + F).\n11. Copy paste/move " \
                 "in your year folder.\n12. Commit the change.\n13. Re-run this program." \
                 "\n\nClicking the 'Return' button takes you back to the Menu.\n\nTo close the program, " \
                 "press the x at the top right of the window.\n\n Have fun! :)"

        # text widget for multiline text
        self.info_window = Text(self.frame, font=font, width=60, height=15, bg=bg, wrap=WORD, padx=20, pady=20)
        self.info_window.grid(row=1)

        # create link that will go in the text box
        self.link = Label(self.info_window, text="https://github.com/MarlingHeli/Manling_3DTP_91906_91907.git",
                          font=font + ("underline",), cursor="hand2", fg="green", bg=bg)
        self.link.bind("<Button-1>", lambda e: self.callback("https://github.com/MarlingHeli/Manling_3DTP_91906_91907"
                                                             ".git"))

        # put text into textbox
        self.info_window.insert(tkinter.END, info_1)
        self.info_window.window_create(tkinter.END, window=self.link)
        self.info_window.insert(tkinter.END, info_2)

        # make the text read only
        self.info_window.config(state=DISABLED)

        # add scrollbar
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.grid(row=1, column=2, sticky="nsew")
        self.scrollbar.config(command=self.info_window.yview)

        # add border for button
        self.return_border = Frame(self.button_frame, highlightbackground="#000000", highlightthickness=1, bd=1)
        self.return_border.grid(row=1, column=2, pady=(20, 10))

        # create button
        self.button_return = Button(self.return_border, text="Return", font=font, bg="#BAFFD3", bd=0,
                                    highlightthickness=5,
                                    command=lambda: [self.frame.destroy(), self.button_frame.destroy(), Menu()])
        self.button_return.grid(row=0)

    def callback(self, url):
        webbrowser.open_new_tab(url)


#######################################################################################################################

if __name__ == "__main__":
    window = Tk()
    window.title("Waka Ama ranking finder")
    window.geometry("700x500")
    window.configure(bg=bg)
    # run Menu class first
    Menu()
    # keep window on screen
    window.mainloop()
