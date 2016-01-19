from DisplayDriver import DisplayDriver
from DisplayDriver.GuiObjects import *
from pygame.locals import *

d = DirectInput(pos = [0,0], text='Input: ')
d.render(DisplayDriver.engine)

DisplayDriver.eventManager.bind(KEYDOWN, d.takeInput)
DisplayDriver.init()