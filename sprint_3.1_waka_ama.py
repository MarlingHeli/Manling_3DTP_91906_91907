from tkinter import *
# from tkinter import ttk
import requests
from concurrent.futures import ThreadPoolExecutor


class Menu:
    def __init__(self):
        #paragraph and button font
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
        self.year_var = IntVar()
        self.year_var.set("")
        self.year_label = Label(self.menu_buttons, text="Enter year:", font=("Arial", "12"), bg="#FAFFFD")
        self.year_entry = Entry(self.menu_buttons, textvariable=self.year_var, font=("Arial", "20"),
                                width=5, bg="#FAFFFD")
        self.year_label.grid(row=2, column=1, pady=(280, 10))
        self.year_entry.grid(row=2, column=2, pady=(280, 10))

        # give buttons a consistent black border
        self.button_ranker_border = Frame(self.menu_buttons, highlightbackground="#000000",
                                          highlightthickness=1, bd=1)
        self.button_ranker_border.grid(row=2, column=3, pady=(280, 10))

        self.button_help_border = Frame(self.menu_buttons, highlightbackground="#000000",
                                        highlightthickness=1, bd=1)
        self.button_help_border.grid(row=2, column=4, pady=(280, 10), padx=50)

        # create buttons
        self.button_ranker = Button(self.button_ranker_border, text="Find",
                                    font=font, bg="#C9FFDB", bd=0, highlightthickness=5,
                                    )
        self.button_ranker.grid(row=2, column=3)

        self.button_help = Button(self.button_help_border, text="Help/information",
                                  font=font, bg="#DAFFC7", bd=0, highlightthickness=5,
                                  )
        self.button_help.grid(row=2, column=4)


class Ranker:
    def __init__(self):
        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()
        ranker_heading = Label(self.frame, text="Ranking Calculator", font="Arial, 20", bg="#FAFFFD")
        ranker_heading.grid()


class Info:
    def __init__(self):
        self.frame = Frame(bg="#FAFFFD")
        self.frame.grid()
        info_heading = Label(self.frame, text="Help/Information", font="Arial, 20", bg="#FAFFFD")
        info_heading.grid()


# keep window on screen
if __name__ == "__main__":
    window = Tk()
    window.title("Waka Ama ranking finder")
    window.geometry("700x500")
    window.configure(bg="#FAFFFD")
    Menu()
    window.mainloop()
