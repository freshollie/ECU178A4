from DisplayDriver.GuiObjects import *
import math
import Globals
import time
import random
import threading

class Route:
    """
    Route object designed for the robot to follow
    """

    def __init__(self, path):
        self.path = path # Store the path
        self.originalPath = path[:] #Take a copy of the stored path
        self.lines = []
        self.finished = False
        for i in range(len(path)-1): # Generate graphical lines representing the paths
            self.lines.append(Line(path[i].getPos(),
                                   path[i+1].getPos(),
                                   colour = [255,0,0], width = 1))

    def getNextPoint(self):
        """
        Returns the next point in route
        """
        if not self.path:
            self.finished = True
            self.reset()

        return self.path.pop(0)

    def getRoute(self):
        return self.path

    def isFinished(self):
        return self.finished

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

    MASS = 1000 # grams

    def __init__(self,
                 homeNode,
                 town,
                 shoppingList):

        # Initialise the rectangle
        Rectangle.__init__(self,
                           pos=homeNode.getPos(),
                           size=[8,8],
                           colour=[255, 0, 0])

        self.shoppingList = shoppingList
        self.homeNode = homeNode
        self.distanceTraveled = 0
        self.fuelUsed = 0
        self.velocity = 400
        self.turnSpeed = 200
        self.town = town
        self.route = None
        self.bearing = 1
        self.angle = 0
        self.setBearing(0)
        self.targetShop = []
        self.calcPath()

        self.status = "Hunt"
        self.shopsVisited = []

    def setBearing(self, bearing):
        """
        Set which way the robot is facing
        """

        bearing %= 360

        self.bearing = bearing
        self.setRotation(self.bearing)

    def consumeFuel(self, distance):
        self.fuelUsed += self.velocity / 112987.3284729384 * distance
        self.distanceTraveled += distance

    def getFuelUsed(self):
        return self.fuelUsed

    def getDistanceTraveled(self):
        return self.distanceTraveled

    def turn(self, targetBearing):
        """
        Turns at the correct turn speed towards the given target bearing
        """

        if abs(self.bearing - targetBearing)<(self.turnSpeed/Globals.FPS):
            # If the angle it needs to turn is less than it would turn this tick
            self.setBearing(targetBearing)
            return

        bearing = self.bearing

        if targetBearing>bearing: # Calculates the optimal direction to turn
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

        self.setBearing(self.bearing+(self.turnSpeed/Globals.FPS*turnModifier)) # Turns in the direction relative to turn speed


    def reccurPath(self, currentShop, previousShops, pathLength, toVisit, lastMatters = False):
        """
        Recur path runs a brute force traveling salesman solution.

        It will return the fastest route around all of the given shops in the order they
        will be navigated
        """

        connectingShops = self.town.getConnections(currentShop) # Find the shops that are connected to the current shop

        highestList = []
        middleList = []
        bottomList = []

        if set(toVisit).issubset(set(previousShops)):
            # If we have visited all the shops we need to
            if lastMatters:
                # If we care about the last shop we visit
                if previousShops[-1] == toVisit[-1]:
                    # Make sure that the last shop we visited was the last shop we need to
                    yield (previousShops[:], pathLength) # Yield the path along with its length
                    return

            else:
                yield (previousShops[:], pathLength)
                return

        testToVisit = toVisit[:]
        del testToVisit[-1]

        if toVisit[-1] in connectingShops and set(testToVisit).issubset(set(previousShops)) and not lastMatters:
            # If we are at the end of the route, then we have found a valid route
            yield (previousShops[:] + [toVisit[-1]], pathLength + previousShops[-1].getPos().getDist(toVisit[-1].getPos()))
            return

        for shop in connectingShops:
            if len(previousShops) > 2:
                shouldContinue = False

                for i in range(len(previousShops)):
                    if i>0:
                        if previousShops[i-1] == currentShop and previousShops[i] == shop:
                            shouldContinue = True

                if shouldContinue:
                    continue

            if len(previousShops)>1:
                if previousShops[-2] == shop:
                    continue

            if shop in previousShops:
                #bottomList.append(shop)
                continue

            if shop in toVisit:
                highestList.append(shop)

            else:
                middleList.append(shop)

        for shop in highestList + middleList + bottomList:

            # New shop found so recur for that shop with new perameters
            paths = self.reccurPath(shop, previousShops[:]+[shop], pathLength + currentShop.getPos().getDist(shop.getPos()), toVisit, lastMatters = lastMatters)

            for path in paths:
                if path != False: # If false is returned then no valid route was found for that shop
                    yield path


        # Run out of shops and we are at the end of the route, so return False show not a valid route
        yield False

    def getRandomShopsToVisit(self):
        newToVisit = []
        toVisit = self.town.getShops()
        toVisit.remove(self.homeNode)

        for i in range(random.randint(1,len(toVisit))):
            shop = random.choice(toVisit)
            shop.setColour([0,0,255])
            newToVisit.append(shop)
            toVisit.remove(shop)

        #toVisit.remove(self.homeNode)
        toVisit = newToVisit

        return toVisit

    def calcPath(self, toVisit = [], lastMatters = False):
        """
        Finds and stores a path around the town to the given shops.
        if no shops are given then a route around the town is found.
        """

        if not self.town:
            # If there is no given town then this won't work so return
            return

        if not toVisit:
            toVisit = self.town.getShops()
            toVisit.remove(self.homeNode)

        currentShop = self.town.getShopFromPosition(self.getPos())

        paths = self.reccurPath(currentShop, [currentShop], 0, toVisit, lastMatters = lastMatters) # Generator object to find all the valid paths

        shortestLength = float("inf")
        shortestPath = None
        startTime = time.time()

        for path in paths:
            # Check each new generated path to find the shortest one
            if not path:
                continue

            if path[1] < shortestLength:
                shortestLength = path[1]
                shortestPath = path[0]

            if time.time()-startTime>30:
                break # Some paths take too long to check (it's O(n!) complexity) so the loop
                      # will stop if 30 seconds passes

        if shortestPath == None:
            return

        if self.route:
            self.route.destroy() # Unrender the previous route

        self.route = Route(shortestPath) # Make a route object of the found path

        if self.rendered:
            self.route.render(self.rendered) # Rendering the path for visual reasons

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
            # Trig works by finding the other 2 sides of the triangle
            # in this case X and Y from the hypotenuse the distance

            if self.bearing < 90:

                yPlus = -(math.cos(math.radians(self.bearing))*distance)
                xPlus = math.sin(math.radians(self.bearing))*distance

            elif self.bearing < 180:

                bearing = math.radians(self.bearing - 90)
                xPlus = math.cos(bearing)*distance
                yPlus = math.sin(bearing)*distance

            elif self.bearing< 270:

                bearing = math.radians(self.bearing - 180)
                xPlus = -math.sin(bearing)*distance
                yPlus = math.cos(bearing)*distance

            elif self.bearing < 360:

                bearing = math.radians(self.bearing - 270)
                xPlus = - math.cos(bearing)*distance
                yPlus = - math.sin(bearing)*distance

        return self.getX()+xPlus, self.getY()+yPlus # Return the new position

    def tick(self):
        """
        Tick method. Called every new displayed frame
        """

        if not self.route: # If there is no defined route nothing can be done
            return

        if self.status == "Hunt" or self.status == "Buy":

            if self.targetShop: # If there is a current targetShop

                if self.getPos().getDist(self.targetShop.getPos())<(self.velocity*Globals.PixelsPerMetre/Globals.FPS):
                    # If the distance to the shop is so small that it will go past it next movement
                    # Then move to the shop
                    self.consumeFuel(self.getPos().getDist(self.targetShop.getPos()))
                    self.setPos(self.targetShop.getPos())

                    self.targetShop = self.route.getNextPoint() # Get a new target shop

                elif self.bearing == self.targetShop.getPos().getBearing(self.getPos()):
                    # If the current bearing is correct
                    self.consumeFuel(self.velocity*Globals.PixelsPerMetre/Globals.FPS)

                    self.setPos(self.calcTrigPos(self.velocity*Globals.PixelsPerMetre/Globals.FPS))

            else:
                self.targetShop = self.route.getNextPoint()

            if self.route.isFinished():

                if self.status == "Hunt":
                    newShops = self.getRandomShopsToVisit()
                    newShops.append(self.homeNode)
                    self.calcPath(newShops, lastMatters = True)
                    self.targetShop = self.route.getNextPoint()
                    self.status = "Buy"

                else:
                    self.status = "Finished"

            self.turn(self.targetShop.getPos().getBearing(self.getPos())) # Turn towards the given bearing

    def destroy(self):
        if self.route:
            self.route.destroy()
        self.removeNode()

    def render(self, renderer):
        if self.route:
            self.route.render(renderer)

        Rectangle.render(self, renderer)



