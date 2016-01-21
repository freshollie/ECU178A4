from DisplayDriver import DisplayUI
from DisplayDriver import DisplayDriver
import random


DisplayDriver.engine.setFrameRate(50)

def doSomething():
    print('Doing something when clicked')

b = DisplayUI.Button(size=[100, 40], text = 'Option 1', pos = [640/2, 480/2], command = doSomething)
b.render(DisplayDriver.engine)
b.register(DisplayDriver.eventManager.buttonManager)

DisplayDriver.init()