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
    def __init__(self, start, end):#
        #size = [10, Point(start).getDist(end)]
        #rotation = Point(start).getBearing(Point(end))

        #self.generateRepresentation(start, end)
        Line.__init__(self, start, end, width = 1)

    def destroy(self):
        self.removeNode()

    def render(self, renderer):
        Line.render(self, renderer)

class Shop(Rectangle):
    def __init__(self, pos, name = 'Shop'):
        self.name = name
        Rectangle.__init__(self, pos, size = [10,10])

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
    def __init__(self, roadSpecification = {}, maxShops = 5):
        self.maxShops = maxShops
        self.roads = []
        self.shopDict = roadSpecification

        if not roadSpecification:
            self.randomlyGenerate()

    def notIntersect(self, line):
        for shop in self.shopDict:
            for otherShop in self.shopDict[shop]:
                a = find_intersection(shop.getPos(), otherShop.getPos(), line[0], line[1])
                if a:
                    #Rectangle(pos = a, size = [20,20], colour = [255,0,0]).render(DisplayDriver.engine)
                    return False
        return True

    def orderDistance(self, fromPoint, toPoints, take=-1):

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

        breakNum = 6

        for i in range(breakNum):
            for shop in orderedShopDict:
                if orderedShopDict[shop]:
                    otherShop = orderedShopDict[shop][0]
                    if otherShop not in self.shopDict[shop] and shop not in self.shopDict[otherShop]:
                        if self.notIntersect([shop.getPos(), otherShop.getPos()]):
                            self.shopDict[shop].append(otherShop)
                            self.shopDict[otherShop].append(shop)

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


class lel():
    def __init__(self):
        self.t = None
        self.mouseText = OnscreenText(pos=[0,0], text = '', size = 20)
        self.mouseText.render(DisplayDriver.engine)

    def new(self, event=None):
        if self.t:
            self.t.destroy()
            self.r.destroy()
        self.t = Town(maxShops=15)
        self.t.render(DisplayDriver.engine)
        self.r = Robot(random.choice(list(self.t.shopDict)), town = self.t)
        self.r.calcPath()
        self.r.render(DisplayDriver.engine)

    def kek(self, event):
        self.mouseText.setPos(event.pos)
        self.mouseText.setText(str(event.pos))

    def tick(self):
        self.r.tick()

l = lel()

l.new()

#DisplayDriver.engine.addTask(l.new, [None])
#DisplayDriver.eventManager.bind(KEYDOWN, l.new)
DisplayDriver.eventManager.bind(MOUSEMOTION, l.kek)

DisplayDriver.engine.addTask(l.tick)


class Simulation():
    def __init__(self):
        self.robot = Robot([640/2,640/2])
        self.robot.render(DisplayDriver.engine)
        #r.setBearing(random.random()*360)

        self.robot.velocity = 100

        #DisplayDriver.eventManager.bind(MOUSEMOTION,mouseMoved)
        DisplayDriver.engine.addTask(r.tick)


    def mouseMoved(event):
        pos = event.pos

        self.robot.setBearing(Point(pos).getBearing(r.getPos()))

DisplayDriver.engine.setFrameRate(Globals.FPS)
DisplayDriver.engine.graphics.setRes(Globals.RESOLUTION)


DisplayDriver.init()

