from DisplayDriver import DisplayUI
from DisplayDriver import DisplayDriver
import random


DisplayDriver.engine.setFrameRate(50)

class MainScreen(object):
    def __init__(self):
        self.option1 = DisplayUI.Button(size=[50, 20], text = 'Option 1', pos = [640/2, 0], command = self.option1Selected)


    def show(self):
        self.option1.render(DisplayDriver.engine)
        self.option1.register(DisplayDriver.eventManager.buttonManager)

    def hide(self):
        self.option1.removeNode()
        self.option1.deregister()


class UITesting(object):
    def __init__(self):
        self.mainScreen = MainScreen()
        self.mainScreen.show()


DisplayDriver.init()