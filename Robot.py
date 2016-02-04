from DisplayDriver.GuiObjects import *
import math
import Globals

class Route:
    """
    Route object designed for the robot to follow
    """

    def __init__(self, path):
        self.path = path
        self.originalPath = path[:]
        self.lines = []
        for i in range(len(path)-1):
            self.lines.append(Line(path[i].getPos(),
                                   path[i+1].getPos(),
                                   colour = [255,0,0], width = 1))

    def getNextPoint(self):
        if not self.path:
            self.reset()

        return self.path.pop()

    def reset(self):
        self.path = self.originalPath[:]

    def render(self, renderer):
        for line in self.lines:
            line.render(renderer)

    def destroy(self):
        for line in self.lines:
            line.removeNode()

class Robot(Rectangle):
    def __init__(self,
                 homeNode,
                 town):

        Rectangle.__init__(self,
                           pos = homeNode.getPos(),
                           size = [20,20],
                           colour = [255, 0, 0])

        self.homeNode = homeNode
        self.velocity = 2000
        self.turnSpeed = 1000
        self.town = town
        self.route = None
        self.bearing = 0
        self.angle = 0
        self.setBearing(0)
        self.targetShop = []
        self.calcPath()
        self.status = "Hunt"

    def setBearing(self, bearing):
        while bearing>=360:
            bearing -= 360

        while bearing<0:
            bearing+=360

        self.bearing = bearing
        self.setRotation(self.bearing)

    def turn(self, targetBearing):
        if abs(self.bearing - targetBearing)<(self.turnSpeed/Globals.FPS):
            self.setBearing(targetBearing)
            return

        turnModifier = (targetBearing-self.bearing)/abs(targetBearing-self.bearing)

        self.setBearing(self.bearing+(self.turnSpeed/Globals.FPS*turnModifier))


    def reccurPath(self, currentShop, previousShops, pathLength):
        connectingShops = self.town.getConnections(currentShop)

        for shop in connectingShops:

            if shop in previousShops:
                continue

            #print(shop, previousShops[:]+[shop], pathLength + currentShop.getPos().getDist(shop.getPos()))
            returnValue = self.reccurPath(shop, previousShops[:]+[shop], pathLength + currentShop.getPos().getDist(shop.getPos()))

            if returnValue != False:
                return returnValue
        if self.homeNode in connectingShops and len(previousShops) == len(self.town.shopDict):
            return (previousShops[:] + [self.homeNode], pathLength + currentShop.getPos().getDist(shop.getPos()))
        else:
            return False


    def calcPath(self):
        if not self.town:
            return
        l = self.reccurPath(self.homeNode, [self.homeNode], 0)
        if l:
            l = l[0]

            self.route = Route(l)

        else:
            print(l)


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
        if self.status == "Hunt":
            if self.targetShop:
                if self.getPos().getDist(self.targetShop.getPos())<(self.velocity*Globals.PixelsPerMetre/Globals.FPS):
                    self.setPos(self.targetShop.getPos())
                    self.targetShop = self.route.getNextPoint()
                elif self.bearing == self.targetShop.getPos().getBearing(self.getPos()):
                    self.setPos(self.calcTrigPos(self.velocity*Globals.PixelsPerMetre/Globals.FPS))

            else:
                self.targetShop = self.route.getNextPoint()
            self.turn(self.targetShop.getPos().getBearing(self.getPos()))

            #self.setPos(self.calcTrigPos(self.velocity*Globals.PixelsPerMetre/Globals.FPS))

    def destroy(self):
        if self.route:
            self.route.destroy()
        self.removeNode()

    def render(self, renderer):
        if self.route:
            self.route.render(renderer)

        Rectangle.render(self, renderer)



