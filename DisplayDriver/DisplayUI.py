from .GuiObjects import *
from .Points import *

class UIObjectBase(object):
    def __init__(self, pos):
        self.pos = Point(pos)

    def updateElementPosition(self):
        pass

    def getPos(self):
        return self.pos.getPos()

    def getX(self):
        return self.pos.getX()

    def getY(self):
        return self.pos.getY()

    def setPos(self, pos):
        self.pos.setPos(pos)
        self.updateElementPositions()

    def setX(self, x):
        self.pos.setX(x)
        self.updateElementPositions()

    def setY(self, y):
        self.pos.setY(y)
        self.updateElementPositions()

    def hoverDown(self):
        pass

    def hoverUp(self):
        pass

    def mouseDown(self):
        pass

    def mouseUp(self):
        pass

    def runCommand(self):
        pass

    def render(self, renderer):
        pass

    def destroy(self):
        pass

    def register(self, uiManager):
        uiManager.register(self)

class Button(UIObjectBase):
    def __init__(self, pos, text='', size = [100,40], textSize = 20, upColour = [0,0,0], downColour  = [255,255,255], textColour = [255,255,255], command=None,):
        self.size = size
        self.command = command
        self.upColour = upColour
        self.downColour = downColour
        self.textColour = textColour
        self.mouseOver = True
        self.buttonManager = None

        UIObjectBase.__init__(self,pos)
        self.text = OnscreenText(text = text, pos = pos, size = textSize, colour = textColour)
        self.background = Rectangle(pos = pos, size = size, colour = upColour, centered = False)
        self.placeText()

    def setText(self, text):
        self.text.setText(text)
        self.placeText()

    def placeText(self):
        sizedText = self.text.font.size(self.text.text)
        print(sizedText)
        plusX = (self.size[0] - sizedText[0])/2
        plusY = (self.size[1] - sizedText[1])/2

        position =  Point(self.getX()+plusX, self.getY()+plusY)
        self.text.setPos(position)

    def updateElementPositions(self):
        self.background.setPos(self.getPos())
        self.placeText(self)

    def render(self, renderer):
        self.background.render(renderer)
        self.text.render(renderer)

    def destroy(self):
        self.background.removeNode()
        self.text.removeNode()

    def runCommand(self):
        if self.mouseOver:
            self.command()

    def hoverDown(self):
        self.text.setColour([255-self.textColour[0],255-self.textColour[1],255-self.textColour[2]])
        self.mouseOver = True

    def hoverUp(self):
        self.text.setColour(self.textColour)
        self.mouseOver = False

    def mouseDown(self):
        self.background.setColour(self.downColour)
        self.hoverDown()

    def mouseUp(self):
        self.background.setColour(self.upColour)
        self.hoverUp()


    def register(self, buttonManager):
        buttonManager.register(self)
        self.buttonManager = buttonManager

    def deregister(self):
        if self.buttonManager:
            self.buttonManager.deregister(self)