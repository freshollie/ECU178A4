import sys
from tkinter import *

class Settings:
    def __init__(self, root):
        self.root = root
        #The Canvas
        self.canvas = Canvas(root, width=700, height= 500, bg='light blue')
        self.canvas.pack()
        #The pink rectangle
        self.canvas.create_rectangle(30,100, 670,470, fill='white')
        #The 'Settings' title
        self.settings = Label(root, text='Settings', font=30)
        self.settingsWindow = self.canvas.create_window(80,40, window = self.settings)
        #The 'Time Limit' label
        self.timeLimit = Label(root, text='Time Limit', font = 20)
        self.timeLimitWindow = self.canvas.create_window(100,150, window = self.timeLimit)
        #The 'Main Menu' button
        self.mainMenu = Button(root, text='Main Menu', width=10)
        self.mainMenuWindow = self.canvas.create_window(600, 40, window = self.mainMenu)



def main():
    root = Tk()
    gui = Settings(root)
    root.mainloop

if __name__ == '__main__':
    sys.exit(main())
