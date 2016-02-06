from DisplayDriver.GuiObjects import *
import math
import Globals
import time

class Route:
    """
    Route object designed for the robot to follow
    """

    def __init__(self, path):
        self.path = path # Store the path
        self.originalPath = path[:] #Take a copy of the stored path
        self.lines = []
        for i in range(len(path)-1): # Generate graphical lines representing the paths
            self.lines.append(Line(path[i].getPos(),
                                   path[i+1].getPos(),
                                   colour = [255,0,0], width = 1))

    def getNextPoint(self):
        """
        Returns the next point in route
        """
        if not self.path:
            self.reset()

        return self.path.pop()

    def reset(self):
        """
        Reset the path so that it can be traversed again
        """
        self.path = self.originalPath[:]

    def render(self, renderer):
        """
        Renders the path so that it can be see on screen
        """
        for line in self.lines:
            line.render(renderer)

    def destroy(self):
        """
        Destroy the path so that it is no longer seen on screen
        """
        for line in self.lines:
            line.removeNode()

class Robot(Rectangle):
    """
    Robot object, represented by a rectangle

    It will find the path around a town and move around that path
    """

    def __init__(self,
                 homeNode,
                 town):

        # Initialise the rectangle
        Rectangle.__init__(self,
                           pos = homeNode.getPos(),
                           size = [20,20],
                           colour = [255, 0, 0])

        #
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
        """
        Set which way the robot is facing
        """

        bearing = bearing % 360

        self.bearing = bearing
        self.setRotation(self.bearing)

    def turn(self, targetBearing):
        """
        Turns at the correct turn speed towards the given target bearing
        """

        if abs(self.bearing - targetBearing)<(self.turnSpeed/Globals.FPS):
            self.setBearing(targetBearing)
            return

        bearing = self.bearing

        if targetBearing>bearing:
            difference = targetBearing - bearing
            if difference > 180:
                turnModifier = -1
            else:
                turnModifier = 1
        else:
            difference = bearing - targetBearing

            if difference > 180:
                turnModifier = 1
            else:
                turnModifier = -1

        self.setBearing(self.bearing+(self.turnSpeed/Globals.FPS*turnModifier))


    def reccurPath(self, currentShop, previousShops, pathLength):
        """
        Reccurr path runs a brute force traveling salesman solution.

        It will return the fastest route around all of the shops in the order they
        will be navigated
        """

        connectingShops = self.town.getConnections(currentShop) # Find the shops that are connected to the current shop

        for shop in connectingShops:

            if shop in previousShops:
                continue # If the selected next shop has already been used it will be ignored

            # New shop found so recur for that shop with new perameters
            returnValue = self.reccurPath(shop, previousShops[:]+[shop], pathLength + currentShop.getPos().getDist(shop.getPos()))

            if returnValue != False: # If false is returned then no valid route was found for that shop
                return returnValue # Return the valid route

        if self.homeNode in connectingShops and len(previousShops) == len(self.town.shopDict):
            # If we are at the end of the route, then we have found a valid route
            return previousShops[:] + [self.homeNode]
        else:
            # Run out of shops and we are at the end of the route, so return False show not a valid route
            return False


    def calcPath(self):
        """
        Finds and stores a path around the town
        """

        if not self.town:
            # If there is no given town then this won't work so return
            return

        path = self.reccurPath(self.homeNode, [self.homeNode], 0)

        if path:
            self.route = Route(path) # Make a route object of the found path

        else:
            print(path)


    def calcTrigPos(self, distance):
        """
        Calculates and returns a new position of the robot
        for the given distance. It uses the bearing of the robot to
        calculate this.

        A bearing of 0 is directly up and rotates clockwise
        """

        # If you did GCSE maths you should understand trig.
        # But if not here is an explantion


        # If the bearing is an exact 90 degrees then there is no need for
        # trig to be used.
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
            # Do the correct trig calculation based on what the bearing is.
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

        return self.getX()+xPlus, self.getY()+yPlus # Return the new position

    def tick(self):
        """
        Tick method. Called every new display frame.

        """

        if self.status == "Hunt": # Hunt means go looking around the shops

            if self.targetShop: # If there is a current targetShop

                if self.getPos().getDist(self.targetShop.getPos())<(self.velocity*Globals.PixelsPerMetre/Globals.FPS):
                    # If the distance to the shop is so small that it will go past it next movement
                    # Then move to the shop

                    self.setPos(self.targetShop.getPos())

                    self.targetShop = self.route.getNextPoint() # Get a new target shop

                elif self.bearing == self.targetShop.getPos().getBearing(self.getPos()):
                    # If the current bearing is correct

                    self.setPos(self.calcTrigPos(self.velocity*Globals.PixelsPerMetre/Globals.FPS))

            else:
                self.targetShop = self.route.getNextPoint()

            self.turn(self.targetShop.getPos().getBearing(self.getPos())) # Turn towards the given bearing

            #self.setPos(self.calcTrigPos(self.velocity*Globals.PixelsPerMetre/Globals.FPS))

    def destroy(self):
        if self.route:
            self.route.destroy()
        self.removeNode()

    def render(self, renderer):
        if self.route:
            self.route.render(renderer)

        Rectangle.render(self, renderer)



