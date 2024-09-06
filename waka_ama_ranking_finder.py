# version with no token
import requests  # send requests to GitHub server to retrieve data
import tkinter.messagebox  # create messagebox for error window
import webbrowser  # take users to the web via hyperlink
from io import BytesIO  # use to add image
from pathlib import Path  # use to find user's local download directory
from tkinter import *  # use for tkinter widgets for GUI
from tkinter import filedialog  # used to open file explorer to save csv file
from PIL import Image, ImageTk  # used to add image

# use GitHub repo for directory
api_url = "https://api.github.com/repos/MarlingHeli/Manling_3DTP_91906_91907/contents/Waka Ama data/3.7B resource files"
img_url = "https://raw.githubusercontent.com/MarlingHeli/Manling_3DTP_91906_91907" \
          "/a1cf182892fb46231a34290740f6c26fd489c216/boating-220066_1280.jpg"

folder_dict = {}

# heading font
heading_font = ("Yu Gothic UI", "22", "bold")
heading_fg = "#315944"
# paragraph and button font
para_font = ("Yu Gothic UI Semibold", "12")
para_fg = "#284A29"
# background colour
bg = "#FAFFFD"
# button colours
outline_clr = "#284A29"
click_clr = "#DAFFC7"


#######################################################################################################################
class Menu:  # menu screen that also error checks input
    def __init__(self):
        # create frames
        self.frame = Frame(bg=bg)
        self.frame.grid(sticky="nsew")
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.error_frame = Frame(bg=bg)
        self.error_frame.grid(row=3, column=0, pady=(5, 0))

        self.button_frame = Frame(bg=bg)
        self.button_frame.grid(row=4, column=0, pady=(5, 25))

        # add text
        self.menu_heading = Label(self.frame, text="Waka Ama ranking finder", font=heading_font, bg=bg, fg=heading_fg)
        self.menu_heading.grid(row=0, pady=(30, 0))

        self.menu_desc = Label(self.frame,
                               text="Welcome to the unofficial Waka Ama ranking finder! Use this program to "
                                    "check the results of a previous competition by year.", font=para_font,
                               wrap=550, width=80, justify="left", bg=bg, pady=10, fg=para_fg)
        self.menu_desc.grid(row=1)

        # add image
        response = requests.get(img_url)
        # check if request was successful
        if response.status_code == 200:
            # open image from image data
            image_data = BytesIO(response.content)
            self.image = Image.open(image_data)
            # copy image which will be used as the new image size when users resize the window
            self.image_copy = self.image.copy()
            self.img = ImageTk.PhotoImage(self.image)

            # store image in a label
            self.img_bg = Label(self.frame, image=self.img)
            self.img_bg.grid(sticky="nsew", padx=50)

            self.img_bg.bind("<Configure>", self.resize_img)
        else:
            img_label = Label(self.frame, text="Failed to load image :(", bg=bg, font=para_font, fg="red")
            img_label.grid(pady=15, padx=10)

        # add entry field for years
        self.year_var = StringVar()
        self.year_var.set("")
        self.year_label = Label(self.button_frame, text="Enter year:", font=para_font, bg=bg, fg=para_fg)
        self.year_entry = Entry(self.button_frame, textvariable=self.year_var, font=("Yu Gothic UI Semibold", "21"),
                                fg=para_fg, width=5, bg=bg, highlightbackground=outline_clr, highlightthickness=1)
        self.year_label.grid(row=0, column=0)
        self.year_entry.grid(row=0, column=1)

        # give buttons a consistent black border
        self.find_border = Frame(self.button_frame, highlightbackground=outline_clr, highlightthickness=1, bd=1)
        self.find_border.grid(row=0, column=2)

        self.help_border = Frame(self.button_frame, highlightbackground=outline_clr, highlightthickness=1, bd=1)
        self.help_border.grid(row=0, column=3, padx=50)

        # create buttons
        self.find_button = Button(self.find_border, text="Find", font=para_font, bg="#BAFFD3", bd=0,
                                  highlightthickness=5, command=self.year_check, fg=para_fg, activebackground=click_clr,
                                  activeforeground=para_fg)
        self.find_button.grid(row=1, column=2)

        self.help_button = Button(self.help_border, text="Help/information", font=para_font, bg="#C9FFDB", bd=0,
                                  highlightthickness=5, fg=para_fg, activebackground=click_clr,
                                  command=lambda: [self.frame.destroy(), self.button_frame.destroy(),
                                                   self.error_frame.destroy(), Info()], activeforeground=para_fg)
        self.help_button.grid(row=1, column=3)

        # add error label
        self.error_label = Label(self.error_frame, text="", font=para_font, fg="red", bg=bg)
        self.error_label.grid(row=0)

    def resize_img(self, event):  # resize image based on window size
        # get new width and height of window
        new_width = event.width
        new_height = event.height

        # resize duplicate image to screen size
        self.image = self.image_copy.resize((new_width, new_height))

        self.img = ImageTk.PhotoImage(self.image)
        # update image size
        self.img_bg.configure(image=self.img)

    def get_directory(self, url, year):  # get contents of 3.7B folder from GitHub directory
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
class Ranker:
    def __init__(self, folder_url, year):  # ranking calculator screen that calculates points
        # create frames
        self.frame = Frame(bg=bg)
        self.frame.grid(sticky="nsew")
        self.frame.rowconfigure(2, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.label_frame = Frame(bg=bg)
        self.label_frame.grid(pady=5)

        self.button_frame = Frame(bg=bg)
        self.button_frame.grid(pady=(5, 25))

        # add text
        self.ranker_heading = Label(self.frame, text=f"Ranking Calculator - {year}", font=heading_font,
                                    bg=bg, fg=heading_fg)
        self.ranker_heading.grid(row=0, pady=(20, 0))

        self.ranker_desc = Label(self.frame, font=para_font, wrap=550, width=80,
                                 justify="left", bg=bg, fg=para_fg)
        self.ranker_desc.grid(row=1, pady=10)

        # create scroll bar
        self.scrollbar = Scrollbar(self.frame, width=21)
        self.scrollbar.grid(row=2, column=1, sticky="ns", padx=(0, 50))

        # create results list
        self.results = Listbox(self.frame, bg="white", width=60, height=11, font=para_font,
                               yscrollcommand=self.scrollbar.set, fg=para_fg)

        # give buttons a consistent black border
        self.csv_border = Frame(self.button_frame, highlightbackground=outline_clr, highlightthickness=1, bd=1)
        self.csv_border.grid(row=0, column=0, padx=50)

        self.return_border = Frame(self.button_frame, highlightbackground=outline_clr, highlightthickness=1, bd=1)
        self.return_border.grid(row=0, column=1, padx=50)

        # create buttons
        self.csv_button = Button(self.csv_border, text="Export to csv", font=para_font, bg="#BAFFD3", bd=0,
                                 highlightthickness=5, activebackground=click_clr, activeforeground=para_fg,
                                 command=lambda: self.export_csv(year), fg=para_fg, state=DISABLED)
        self.csv_button.grid(row=0, column=0)
        # return to menu
        self.return_button = Button(self.return_border, text="Return", fg=para_fg,
                                    font=para_font, bg="#C9FFDB", bd=0, highlightthickness=5,
                                    activebackground=click_clr, activeforeground=para_fg,
                                    command=lambda: [self.frame.destroy(), self.button_frame.destroy(),
                                                     self.label_frame.destroy(), Menu()])
        self.return_button.grid(row=0, column=1)

        # add error/processing label
        self.label = Label(self.label_frame, text="", font=para_font, fg=para_fg, bg=bg)
        self.label.grid(row=0)

        # update screen
        self.frame.update()

        # run folder_reader method
        try:
            self.folder_reader(folder_url)
            # detect if users want to exit
        except TclError:
            return

    def points_calculator(self, place, name, dictionary):  # assign points based on place number
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
        if name not in dictionary:
            dictionary[name] = 0

        # give 0 points to disqualified teams
        if place == "DNS" or place == "DQ" or place == "Disqualified":
            dictionary[name] += 0
            # print("points: +0")
        else:
            # retrieve points based on place number and add to ranking_dict.
            # retrieves 1 point if place number is not in points_dict.
            dictionary[name] += points_dict.get(place, 1)

            return dictionary

    def file_reader(self, file_name, file_url, dictionary):  # filters for place number and regional name
        response = requests.get(file_url)

        if response.status_code == 200:
            self.label.config(text=f"Processing {file_name}")
            self.frame.update()
            contents = response.text.strip().split("\n")
            # skip the first line
            for record in contents[1:]:
                # split line into items at commas
                line = record.split(",")
                # check for empty place
                if line[0] != "" and line[5] != "":
                    self.points_calculator(line[0], line[5], dictionary)
        else:
            self.label.config(text="Failed to get file contents :(", fg="red")
            self.frame.update()

    # organise ranking dictionary and display it
    def ranking_results(self, dictionary):
        # print ranking results in descending order
        refined_ranking = dict(sorted(dictionary.items(), key=lambda item: item[1], reverse=True))
        # remove loading text
        self.results.delete(0, tkinter.END)
        self.results.insert(0, "Place, Association, Points")
        index = 1
        for key, value in refined_ranking.items():
            self.results.insert(index, f"{index}, {key}, {value}")
            index += 1

    def folder_reader(self, year_url):  # filters for and gets number of final files
        final_files_dict = {}
        ranking_dict = {}
        response = requests.get(year_url)
        if response.status_code == 200:
            # get contents of year folder
            contents = response.json()

            # filter for final files
            for file in contents:
                if "Final" in file["name"]:
                    # get download url for each final file
                    final_files_dict[file["name"]] = file["download_url"]

            # count number of files
            self.ranker_desc.config(text=f"Below is a preview of the rankings. To download the file as a .csv file,"
                                         f" click 'Export to csv'. Number of items in folder: {len(contents)}. Number "
                                         f"of final files: {len(final_files_dict)}")
            # place elements in descending order on screen
            self.results.grid(row=2, column=0, sticky="nsew", padx=(50, 0))
            # tell users that the listbox is loading
            self.results.insert(0, "Loading, please wait...")
            self.scrollbar.config(command=self.results.yview)
            self.frame.update()

            # run file reader for each final file
            for key, value in final_files_dict.items():
                self.file_reader(key, value, ranking_dict)
            self.ranking_results(ranking_dict)
            # clear processing label
            self.label.config(text="")
            # enable csv button when results are done processing
            self.csv_button.config(state=NORMAL)
        else:
            self.label.config(text="Failed to get folder contents :(", fg="red")

    def export_csv(self, year):  # download results as csv file
        try:
            # get user's download path
            downloads = str(Path.home() / "Downloads")
            file_name = f"WakaAmaRanking{year}"
            csv = filedialog.asksaveasfile(initialdir=downloads, filetypes=[("csv file", "*.csv")], mode="w",
                                           initialfile=file_name, defaultextension=".csv")

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
class Info:  # information and tutorial screen
    def __init__(self):
        # create frames
        self.frame = Frame(bg=bg, padx=50)
        self.frame.grid(sticky="nsew")
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.button_frame = Frame(bg=bg)
        self.button_frame.grid(sticky="nsew", pady=(5, 10))
        self.button_frame.rowconfigure(0, weight=1)
        self.button_frame.columnconfigure(0, weight=1)

        # add text
        self.info_heading = Label(self.frame, text="Help/Information", font=heading_font, bg=bg, fg=heading_fg)
        self.info_heading.grid(row=0, pady=(30, 15))

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
                 " go to this repository on GitHub:\n"

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
                 "press the x at the top right of the window.\n\nHave fun! :)\n\nCover image by " \
                 "PublicDomainPictures on Pixabay."

        # add scrollbar
        self.scrollbar = Scrollbar(self.frame, width=21)
        self.scrollbar.grid(row=1, column=1, sticky="nsew")

        # text widget for multiline text
        self.info_window = Text(self.frame, font=para_font, width=60, height=13, bg="white", wrap=WORD, padx=20,
                                pady=20,
                                yscrollcommand=self.scrollbar.set, fg=para_fg)
        self.info_window.grid(row=1, sticky="nsew")

        # create link that will go in the text box
        self.link = Label(self.info_window, text="https://github.com/MarlingHeli/Manling_3DTP_91906_91907.git",
                          font=para_font + ("underline",), cursor="hand2", fg="green", bg=bg)
        self.link.bind("<Button-1>", lambda e: self.callback("https://github.com/MarlingHeli/Manling_3DTP_91906_91907"
                                                             ".git"))

        # put text into textbox
        self.info_window.insert(tkinter.END, info_1)
        self.info_window.window_create(tkinter.END, window=self.link)
        self.info_window.insert(tkinter.END, info_2)

        # make the text read only
        self.info_window.config(state=DISABLED)

        self.scrollbar.config(command=self.info_window.yview)

        # add border for button
        self.return_border = Frame(self.button_frame, highlightbackground=outline_clr, highlightthickness=1, bd=1)
        self.return_border.grid(row=0, pady=(20, 10))

        # create button
        self.return_button = Button(self.return_border, text="Return", font=para_font, bg="#BAFFD3", bd=0,
                                    highlightthickness=5, fg=para_fg, activebackground=click_clr,
                                    activeforeground=para_fg,
                                    command=lambda: [self.frame.destroy(), self.button_frame.destroy(), Menu()])
        self.return_button.grid(row=0)

    def callback(self, url):  # open the hyperlink online
        webbrowser.open_new_tab(url)


#######################################################################################################################

if __name__ == "__main__":
    window = Tk()
    window.title("Waka Ama ranking finder")
    # set window size
    window.geometry("700x500")
    # set minimum window size
    window.minsize(750, 550)
    window.configure(bg=bg)
    # let window adjust size
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    Menu()
    # keep window on screen
    window.mainloop()
