import sys
from tkinter import *

counter = None

def main(window=None):

    global counter

    def Close():
        window.destroy()
    
    if window == None:
        window = Tk()

    window.resizable(width=FALSE, height=FALSE)

    #The Canvas
    canvas = Canvas(window, width=700, height= 500, bg='#E0EBFF')
    canvas.pack()

    #The 'Settings' title
    settings = Label(window, text='Settings', bg='#E0EBFF', font=("Helvetica", 28))
    settingsWindow = canvas.create_window(80,40, window = settings)

    #The 'Time Limit' label
    timeLimit = Label(window, text='Time Limit', bg='white', font=("Helvetica", 20))
    timeLimitWindow = canvas.create_window(100,150, window = timeLimit)

    #The 'Main Menu' button
    mainMenu = Button(window, text='Main Menu', command = Close, font=("Helvetica", 16), bg='white', height=1, width=13)
    mainMenuWindow = canvas.create_window(600, 40, window = mainMenu)

    #The pink rectangle
    canvas.create_rectangle(30,100, 670,470, fill='white')
    #canvas.create_rectangle(30,30, 150,80, fill='white')


    #The incresing integer

    counter = IntVar()
    
    def Increase():
        counter.set(counter.get() + 1)

    value = Label(window, textvariable=counter)
    valueWindow = canvas.create_window(550,150, window = value)
    increaseButton = Button(window, text="Increase", command=Increase, fg="green", bg = "white")
    increaseButtonWindow = canvas.create_window(600,150, window = increaseButton)

    #The decresing integer

    def Decrease():
        counter.set(counter.get() - 1)

    value = Label(window, textvariable=counter)
    valueWindow = canvas.create_window(550,150, window = value)
    decreaseButton = Button(window, text="Decrease", command=Decrease, fg="red", bg = "white")
    decreaseButtonWindow = canvas.create_window(500,150, window = decreaseButton)
