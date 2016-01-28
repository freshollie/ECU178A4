from DisplayDriver.GuiObjects import *
import math
import Globals

class Robot(Rectangle):
    def __init__(self, pos):
        self.velocity = 10
        Rectangle.__init__(self, pos=pos, size = [20,20])

    def setBearing(self, bearing):
        while bearing>=360:
            bearing -= 360
        self.bearing = bearing
        self.setRotation(self.bearing)

    def calcTrigPos(self, distance):

        if self.bearing == 0:
            yPlus = -distance
            xPlus = 0
        elif self.bearing == 90:
            xPlus = distance
            yPlus = 0
        elif self.bearing == 180:
            yPlus = distance
            xPlus = 0
        elif self.bearing == 270:
            xPlus = -distance
            yPlus = 0
        else:
            if self.bearing<90:
                yPlus = -(math.cos(math.radians(self.bearing))*distance)
                xPlus = math.sin(math.radians(self.bearing))*distance
            elif self.bearing<180:
                bearing = math.radians(self.bearing - 90)
                xPlus = math.cos(bearing)*distance
                yPlus = math.sin(bearing)*distance
            elif self.bearing<270:
                bearing = math.radians(self.bearing - 180)
                xPlus = -math.sin(bearing)*distance
                yPlus = math.cos(bearing)*distance
            elif self.bearing<360:
                bearing = math.radians(self.bearing - 270)
                xPlus = - math.cos(bearing)*distance
                yPlus = - math.sin(bearing)*distance

        return self.getX()+xPlus, self.getY()+yPlus

    def tick(self):
        self.setPos(self.calcTrigPos(self.velocity*Globals.PixelsPerMetre/Globals.FPS))



