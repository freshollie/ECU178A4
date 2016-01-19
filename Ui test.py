from DisplayDriver import DisplayUI
from DisplayDriver import DisplayDriver
import random

DisplayDriver.engine.setFrameRate(50)

def t():
    b = DisplayUI.Button(size = [100,20], text='Click Me', pos = [random.random()*640,random.random()*480], command = t)
    b.render(DisplayDriver.engine)
    b.register(DisplayDriver.eventManager.buttonManager)


b = DisplayUI.Button(size = [100,20], text='Click Me', pos = [200,200], command = t)
b.render(DisplayDriver.engine)
b.register(DisplayDriver.eventManager.buttonManager)

DisplayDriver.init()