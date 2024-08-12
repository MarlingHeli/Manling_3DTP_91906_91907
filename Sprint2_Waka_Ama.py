import tkinter as tk
from tkinter import ttk


#parent class that sets up the window and switches between frames (menu, ranker, info)
class Main(tk.Tk):
    #init function for Main class
    def __init__(self, *args, **kwargs):
        #init function for Tk class
        tk.Tk.__init__(self, *args, **kwargs)

        # create main window
        # set window size
        self.geometry("700x500")
        #put frame in a container
        container = tk.Frame(self)
        container.grid()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #dictionary to keep track of frames
        self.frames = {}

        for F in (Menu, Ranker, Info):
            frame = F(container, self)
            #initialise frames
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        # display menu class frame first
        self.show_frame(Menu)

    # method to display a specific frame
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        #set window title based on frame
        if cont == Menu:
            self.title("Menu")
        elif cont == Ranker:
            self.title("Ranking Calculator")
        elif cont == Info:
            self.title("Help/Information")

    #create class for menu screen and include all its components.
class Menu(tk.Frame): #inherit from tk.Frame
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # give buttons their own grid
        menu_buttons = tk.Frame()
        menu_buttons.grid()

        menu_heading = tk.Label(self,
                                text="Waka Ama ranking finder",
                                font=("Arial", "22", "bold"))
        menu_heading.grid(row=0, pady=(60, 10))
        # add description
        menu_description = tk.Label(self,
                                    text="Welcome to the unofficial Waka Ama ranking finder! "
                                         "Use this program to check the results of the 2017 "
                                         "or 2018 competition.",
                                    font=("Arial", "11"),
                                    wrap=530, width=80, justify="left")
        menu_description.grid(row=1)

        # give buttons a consistent black border
        button_2017_border = tk.Frame(menu_buttons, highlightbackground="#000000",
                                      highlightthickness=1, bd=1)
        button_2017_border.grid(row=2, column=0, pady=(280, 10), padx=30)

        button_2018_border = tk.Frame(menu_buttons, highlightbackground="#000000",
                                      highlightthickness=1, bd=1)
        button_2018_border.grid(row=2, column=1, pady=(280, 10), padx=30)

        button_help_border = tk.Frame(menu_buttons, highlightbackground="#000000",
                                      highlightthickness=1, bd=1)
        button_help_border.grid(row=2, column=2, pady=(280, 10), padx=30)

        # create buttons
        button_2017 = tk.Button(button_2017_border, text="2017 competition",
                                font=("Arial", "11"), bg="#BAFFD3", bd=0, highlightthickness=5,
                                command=lambda:controller.show_frame(Ranker))
        button_2017.grid(row=2, column=0)

        button_2018 = tk.Button(button_2018_border, text="2018 competition",
                                font=("Arial", "11"), bg="#C9FFDB", bd=0, highlightthickness=5,
                                command=lambda:controller.show_frame(Ranker))
        button_2018.grid(row=2, column=1)

        button_help = tk.Button(button_help_border, text="Help/information",
                                font=("Arial", "11"), bg="#DAFFC7", bd=0, highlightthickness=5,
                                command=lambda:controller.show_frame(Info))
        button_help.grid(row=2, column=2)

class Ranker(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        ranker_heading = ttk.Label(self, text="Ranking Calculator", font="Arial, 20")
        ranker_heading.grid()

class Info(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        info_heading = ttk.Label(self, text="Help/Information", font="Arial, 20")
        info_heading.grid()


#keep window on screen
window = Main()
window.mainloop()
