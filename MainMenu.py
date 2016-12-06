import sys
from tkinter import *

import Settings
import GuiShoppingList


root = Tk()

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.MainMenuText = Label(self.root, text='Main Menu', font=("Helvetica", 28), bg='#E0EBFF')
        self.MainMenuText.pack(pady=20)

        Button(self.root, text='Run Simulation', font=("Helvetica", 16), bg='white', height=1, width=13, command = runSimulation).pack(pady=80)
        Button(self.root, text='Settings', font=("Helvetica", 16), bg='white', height=1, width=13, command = runSettings).pack(side=TOP)


def main():
    root.resizable(width=FALSE, height=FALSE)
    #Disable resizing
    gui = MainMenu(root)
    root.geometry('{}x{}'.format(700, 500))
    #Set window size
    BackgroundColour = '#E0EBFF'
    root.configure(bg=BackgroundColour)
    #Changes background colour to off white
    root.wm_title("Virtual Robot Bargain Hunt")
    #Changes window title
    root.mainloop()


def runSimulation():
    GuiShoppingList.main()

def runSettings():
    Settings.main(Toplevel())


main()
