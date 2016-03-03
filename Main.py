from DisplayDriver import DisplayDriver
from DisplayDriver.GuiObjects import *
from DisplayDriver.Points import *
from DisplayDriver.Intervals import *
from pygame.locals import *
from Robot import Robot
from DisplayDriver.Points import Point
import random
import Globals
import math
import ItemHandler as itemHandler

SIMSPEED = 1


FPS = 50

def ang(points):
    if len(points) == 3:
            x = points[0].getDist(points[2])
            y = points[0].getDist(points[1])
            z = points[1].getDist(points[2])
            return math.degrees(math.acos((x**2 - y**2 - z**2)/(-2.0 * z * y)))

def find_intersection(p0, p1, p2, p3):
    """
    Find intersection takes the start and end points of 2 lines and
    returns the intersection point if they collide

    Function was found on stackoverflow but modified for our use
    """

    p0,p1,p2,p3 = map(tuple, [p0, p1, p2, p3])
    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]

    denom = s10_x * s32_y - s32_x * s10_y

    if denom == 0 : return None # collinear

    denom_is_positive = denom > 0

    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]

    s_numer = s10_x * s02_y - s10_y * s02_x

    if (s_numer < 0) == denom_is_positive : return None # no collision

    t_numer = s32_x * s02_y - s32_y * s02_x

    if (t_numer < 0) == denom_is_positive : return None # no collision

    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision


    t = t_numer / denom

    intersection_point = ( p0[0] + (t * s10_x), p0[1] + (t * s10_y) )
    roundedPointsx = map(round, [p0[0], p1[0], p2[0], p3[0]], [0]*4)
    roundedPointsy = map(round, [p0[1], p1[1], p2[1], p3[1]], [0]*4)

    roundedPoints = list(zip(roundedPointsx, roundedPointsy))

    if (round(intersection_point[0], 0), round(intersection_point[1], 0)) not in roundedPoints:
        return intersection_point

class Road(Line):
    """
    Road is the representation of a straight road in the town.
    """

    def __init__(self,
                 start,
                 end):

        #size = [10, Point(start).getDist(end)]
        #rotation = Point(start).getBearing(Point(end))

        #self.generateRepresentation(start, end)
        Line.__init__(self, start, end, width = 4, colour = [61, 61, 41])

    def destroy(self):
        self.removeNode()

    def render(self, renderer):
        Line.render(self, renderer)

class Shop(Rectangle):
    """
    Shop is the representation of a shop in the town. May be used later
    if we wanted to find our way around a shop too.
    """
    def __init__(self,
                 pos,
                 category,
                 items):

        self.category = category
        self.items = {}
        self.randomisePrices(items)
        self.home = False


        Rectangle.__init__(self,
                           pos,
                           size = [random.randint(-15, 15) + 30, random.randint(-15, 15) + 30])

        self.text = OnscreenText(text = self.category, size = 15, pos = [pos[0]-15, pos[1]-40], colour = [255,0,0])

    def randomisePrices(self, items):
        modifier = 1 + (5-random.random()*10)

        for item in items:
            self.items[item] = round(item.price * modifier, 2)

    def getItems(self):
        return self.items

    def setCategory(self, category):
        self.category = category
        self.text.setText(self.category)

    def getCategory(self):
        return self.category

    def destroy(self):
        self.removeNode()
        self.text.removeNode()

    def setHome(self):
        self.setCategory("Home")
        self.items = None
        self.setColour([0,255,0])
        self.home = True

    def isHome(self):
        return self.home

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if not self.isHome():
            return "Shop(%s, %s)" %(self.getPos(), self.category)
        else:
            return "Home(%s, %s)" %(self.getPos(), self.category)

    def render(self, renderer):
        Rectangle.render(self, renderer)
        self.text.render(renderer)

    #def render(self, renderer):
     #   Rectangle.render(self, renderer)


class Town(object):
    """
    Town is graph made up of shops connecting to roads.
    """
    def __init__(self,
                 roadSpecification = {},
                 maxShops = 5,
                 categories = []):

        self.maxShops = maxShops
        self.roads = []
        self.shopDict = roadSpecification
        self.categories = categories
        self.home = None

        if not roadSpecification:
            self.randomlyGenerate()

    def notIntersect(self, line):
        """
        Returns true if the road given does not intersect with any other already defined road
        """

        for shop in self.shopDict:
            for otherShop in self.shopDict[shop]:

                a = find_intersection(shop.getPos(), otherShop.getPos(), line[0], line[1])

                if a:
                    #Rectangle(pos = a, size = [20,20], colour = [255,0,0]).render(DisplayDriver.engine)
                    return False
        return True

    def notSmallAngle(self, line):
        """
        Returns true if the road isn't at a really small angle with another road
        """

        for shop in self.shopDict:
            for otherShop in self.shopDict[shop]:
                a = float("inf")

                if line[1] == otherShop.getPos():
                    a = ang([line[0], otherShop.getPos(), shop.getPos()])

                elif line[0] == otherShop.getPos():
                    a = ang([line[1], otherShop.getPos(), shop.getPos()])

                elif line[0] == shop.getPos():
                    a = ang([line[1], shop.getPos(), otherShop.getPos()])

                elif line[1] == shop.getPos():
                    a = ang([line[0], shop.getPos(), otherShop.getPos()])

                if a < 30:
                    print(line, otherShop, shop)
                    #Line(start = line[0], end = line[1], colour = [0,255,0]).render(DisplayDriver.engine)
                    #Line(start = otherShop.getPos(), end = shop.getPos(), colour = [0,255,0]).render(DisplayDriver.engine)
                    return False

        return True

    def orderDistance(self, fromPoint, toPoints, take=-1):
        """
        Returns the list of "toPoints" in ascending order of distance away from "fromPoint"
        """

        smallestOrder = []

        while len(smallestOrder) < len(toPoints)+take:
            smallestDistance = float("inf")
            smallestDistancePoint = None

            for otherPoint in toPoints:
                if fromPoint.getPos().getDist(otherPoint.getPos())<smallestDistance and otherPoint!=fromPoint and otherPoint not in smallestOrder:
                    smallestDistancePoint = otherPoint
                    smallestDistance = fromPoint.getPos().getDist(otherPoint.getPos())

            if smallestDistancePoint:
                smallestOrder.append(smallestDistancePoint)

        return smallestOrder


    def randomlyGenerate(self):
        """
        Randomly generates a graph with the number with max number of shop where all shops are connected to their closest
        shops with no overlapping lines
        """

        self.shopDict = {}
        orderedShopDict = {}

        """
        First Generate all the shop and make sure the distance between them in large
        enough to be viewable
        """

        for i in range(self.maxShops):
            newShop = True

            while newShop:
                p = Point([random.random()*Globals.RESOLUTION[0], random.random()*Globals.RESOLUTION[0]])

                newShop = False

                #Make sure intersections are distenced

                for shop in self.shopDict:
                    if abs(shop.getX() - p.getX()) < Globals.RESOLUTION[0]/self.maxShops/2 or abs(shop.getY() - p.getY()) < Globals.RESOLUTION[0]/self.maxShops/2:
                        newShop = True

            category = random.choice(itemHandler.getCategories())
            items = itemHandler.getItemsFromCategory(category)
            self.shopDict[Shop(p, category, items)]=[]

        """
        Then order all the points in order of distance
        """

        for shop in self.shopDict:
            orderedShopDict[shop] = self.orderDistance(shop, self.shopDict)

        """
        Then connect the points to their closest points without overlapping lines
        and store these connections
        """
        shouldBreak = False
        while not shouldBreak:
            shouldBreak = True
            for shop in orderedShopDict:
                if orderedShopDict[shop]:
                    otherShop = orderedShopDict[shop][0]
                    if otherShop not in self.shopDict[shop] and shop not in self.shopDict[otherShop]:
                        if self.notIntersect([shop.getPos(), otherShop.getPos()]) and self.notSmallAngle([shop.getPos(), otherShop.getPos()]):
                            self.shopDict[shop].append(otherShop)
                            self.shopDict[otherShop].append(shop)
                            shouldBreak = False

                    del orderedShopDict[shop][0]


        """
        Then order those points into order of distance for better searching
        """

        for shop in self.shopDict:
            self.shopDict[shop] = self.orderDistance(shop, self.shopDict[shop], take=0)

        """
        Finally generate the roads based on those connections
        """

        self.roads = []
        alreadyDone = []
        for shop in self.shopDict:
            for otherShop in self.shopDict[shop]:
                if (otherShop, shop) not in alreadyDone:
                    self.roads.append(Road(start = shop.getPos(), end = otherShop.getPos()))
                    alreadyDone.append((shop, otherShop))

        self.home = random.choice(list(self.shopDict.keys()))
        self.home.setHome()

    def getConnections(self, node):
        """
        Returns all the nodes connected by roads to the given node
        """

        if node not in self.shopDict:
            return []

        return self.shopDict[node]

    def getShops(self):
        return list(self.shopDict.keys())

    def getHome(self):
        return self.home

    def getShopFromPosition(self, position):
        for shop in self.shopDict:
            if position.getDist(shop.getPos())<1:
                return shop

        return False

    def render(self, renderer):
        for road in self.roads:
            road.render(DisplayDriver.engine)

        for shop in self.shopDict:
            shop.render(DisplayDriver.engine)

    def destroy(self):
        for shop in self.shopDict:
            shop.destroy()
        for road in self.roads:
            road.destroy()

class Simulation:
    def __init__(self, items = {}):
        DisplayDriver.eventManager.bind(KEYDOWN, self.takeInput)
        DisplayDriver.engine.graphics.setBackground([51,204,51])
        itemHandler.init(False)
        if not items:
            self.items = {}

            items = itemHandler.getItemsSorted(0, False)
            for i in range(random.randint(3,15)):
                item = random.choice(items)
                items.remove(item)
                self.items[item] = random.randint(1,3)
        else:
            self.items = items

        self.taskId = None
        self.generate()
        self.start()

    def getShoppingList(self):
        return self.items

    def tick(self):
        for i in range(SIMSPEED):
            if not self.robot:
                return

            if self.robot.status == "Finished":
                DisplayDriver.engine.removeTask(self.taskId)
                self.taskId = None
                return

            self.robot.tick()
            self.distanceText.setText('Distance: %sm' %(int(self.robot.getDistanceTraveled())))
            self.consumeText.setText('Fuel Used: %s' %(int(self.robot.getFuelUsed())))

            try:
                self.contraintsText.setText('Distance/Fuel: %s' %(round(self.robot.getDistanceTraveled()/self.robot.getFuelUsed(), 2)))
            except ZeroDivisionError:
                pass

    def generate(self):

        self.town = Town(maxShops = 13)
        self.town.render(DisplayDriver.engine)

        self.robot = Robot(town = self.town, shoppingList = self.getShoppingList())
        self.robot.render(DisplayDriver.engine)

        self.consumeText = OnscreenText(pos = [Globals.RESOLUTION[0]-200,0], text = '', size = 20)
        self.consumeText.render(DisplayDriver.engine)

        self.distanceText = OnscreenText(pos = [Globals.RESOLUTION[0]-200,20], text = '', size = 20)
        self.distanceText.render(DisplayDriver.engine)

        self.contraintsText = OnscreenText(pos = [Globals.RESOLUTION[0]-200,30], text = '', size = 20)
        self.contraintsText.render(DisplayDriver.engine)

    def takeInput(self, event):
        if event.key == K_a:
            self.reset()

    def destroy(self):
        if self.robot.route:
            self.robot.route.destroy()
            self.robot.route = None

        if self.taskId:
            DisplayDriver.engine.removeTask(self.taskId)
            self.taskId = None
        self.consumeText.removeNode()
        self.distanceText.removeNode()
        self.robot.destroy()
        self.town.destroy()
        self.contraintsText.removeNode()

        if self.taskId:
            DisplayDriver.engine.removeTask(self.taskId)

    def reset(self):
        if self.robot.route:
            self.robot.route.destroy()
            self.robot.route = None

        while not self.robot.route:
            self.destroy()

            self.generate()
            self.start()


    def start(self):
        self.taskId = DisplayDriver.engine.addTask(self.tick)

def main(shoppingList = {}):

    sim = Simulation(shoppingList)

    DisplayDriver.engine.setFrameRate(Globals.FPS)
    DisplayDriver.engine.graphics.setRes(Globals.RESOLUTION)


    DisplayDriver.init()

if __name__ == "__main__":
    main()

