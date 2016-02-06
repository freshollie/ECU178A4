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

FPS = 50

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
        Line.__init__(self, start, end, width = 1)

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
                 name = 'Shop'):

        self.name = name

        Rectangle.__init__(self,
                           pos,
                           size = [10,10])

    def setName(self, name):
        self.name = name

    def destroy(self):
        self.removeNode()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.getPos())
    #def render(self, renderer):
     #   Rectangle.render(self, renderer)


class Town(object):
    """
    Town is graph made up of shops connecting to roads.
    """
    def __init__(self,
                 roadSpecification = {},
                 maxShops = 5):

        self.maxShops = maxShops
        self.roads = []
        self.shopDict = roadSpecification

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

    def orderDistance(self, fromPoint, toPoints, take=-1):
        """
        Returns the list of "toPoints" in ascending order of distance away from "fromPoint"
        """

        smallestOrder = []

        while len(smallestOrder)<len(toPoints)+take:
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

            self.shopDict[Shop(p)]=[]

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
                        if self.notIntersect([shop.getPos(), otherShop.getPos()]):
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
        alreadyDone =[]
        for shop in self.shopDict:
            for otherShop in self.shopDict[shop]:
                if (otherShop, shop) not in alreadyDone:
                    self.roads.append(Road(start = shop.getPos(), end = otherShop.getPos()))
                    alreadyDone.append((shop, otherShop))

    def getConnections(self, node):
        """
        Returns all the nodes connected by roads to the given node
        """

        if node not in self.shopDict:
            return []

        return self.shopDict[node]

    def render(self, renderer):
        for shop in self.shopDict:
            shop.render(DisplayDriver.engine)

        for road in self.roads:
            road.render(DisplayDriver.engine)

    def destroy(self):
        for shop in self.shopDict:
            shop.destroy()
        for road in self.roads:
            road.destroy()


class Simulation():
    def __init__(self):
        self.town = Town(maxShops = 15)
        self.town.render(DisplayDriver.engine)
        self.robot = Robot(random.choice(list(self.town.shopDict)), town = self.town)
        self.robot.render(DisplayDriver.engine)

    def tick(self):
        self.robot.tick()

class lel():
    def __init__(self):
        self.t = None
        self.rs = []
        self.mouseText = OnscreenText(pos=[0,0], text = '', size = 20)
        self.mouseText.render(DisplayDriver.engine)

    def new(self, event=None):
        if event == None or event.key != K_a:
            if self.t:
                self.t.destroy()
            for r in self.rs:
                r.destroy()
            self.t = Town(maxShops=15)
            self.t.render(DisplayDriver.engine)
        else:
            if self.t:
                self.rs.append(Robot(random.choice(list(self.t.shopDict)), town = self.t))
                self.rs[-1].render(DisplayDriver.engine)


    def kek(self, event):
        self.mouseText.setPos(event.pos)
        self.mouseText.setText(str(event.pos))

    def tick(self):
        for r in self.rs:
            r.tick()

#l = lel()

#l.new()

#DisplayDriver.engine.addTask(l.new, [None])
#DisplayDriver.eventManager.bind(KEYDOWN, l.new)
#DisplayDriver.eventManager.bind(MOUSEMOTION, l.kek)


sim = Simulation()

DisplayDriver.engine.addTask(sim.tick)

DisplayDriver.engine.setFrameRate(Globals.FPS)
DisplayDriver.engine.graphics.setRes(Globals.RESOLUTION)


DisplayDriver.init()

