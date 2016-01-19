class UIManager(object):
    def __init__(self):
        self.elements = []

    def mouseDownEvent(self, event):
        pass

    def mouseUpEvent(self, event):
        pass

    def mouseMotionEvent(self, event):
        pass

    def keyDownEvent(self, event):
        pass

    def keyUpEvent(self, event):
        pass

    def register(self, element):
        if element not in self.elements:
            self.elements.append(element)

    def deregister(self, element):
        self.elements.remove(element)


class ButtonManager(UIManager):
    def __init__(self):
        self.hoveredElement = None
        UIManager.__init__(self)


    def isInClickArea(self, element, pos):
        backgroundImage = element.background.image

        if backgroundImage.collidepoint(pos):
            return True
        else:
            return False

    def getHoveredElement(self,pos):
        for element in self.elements:
            if self.isInClickArea(element, pos):
                return element
        return False


    def mouseDownEvent(self, event):
        element = self.getHoveredElement(event.pos)
        if element:
            if self.hoveredElement:
                self.hoveredElement.mouseUp()
            element.mouseDown()


    def mouseUpEvent(self, event):
        element = self.getHoveredElement(event.pos)
        if element:
            if self.hoveredElement == element:
                element.runCommand()
            element.mouseUp()

    def mouseMotionEvent(self, event):
        element = self.getHoveredElement(event.pos)
        if element:
            if element!=self.hoveredElement:
                element.hoverDown()
                self.hoveredElement = element
        else:
            if self.hoveredElement:
                self.hoveredElement.hoverUp()
                self.hoveredElement = None