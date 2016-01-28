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
        print(round(intersection_point[0], 0), round(intersection_point[1], 0))
        print(roundedPoints)
        return intersection_point

class Road(Line):
    def __init__(self, start, end):#
        #size = [10, Point(start).getDist(end)]
        #rotation = Point(start).getBearing(Point(end))

        #self.generateRepresentation(start, end)
        Line.__init__(self, start, end, width = 1)

class Town(object):
    def __init__(self, roadSpecification = {}, maxIntersections = 5):
        self.maxIntersections = maxIntersections
        self.roads = []
        self.intersectionDict = roadSpecification

        if not roadSpecification:
            self.randomlyGenerate()

    def notIntersect(self, line):
        for point in self.intersectionDict:
            for otherPoint in self.intersectionDict[point]:
                a = find_intersection(point, otherPoint, line[0], line[1])
                if a:
                    #Rectangle(pos = a, size = [20,20], colour = [255,0,0]).render(DisplayDriver.engine)
                    return False
        return True


    def randomlyGenerate(self):
        self.intersectionDict = {}
        smallestPointDict = {}

        for i in range(self.maxIntersections):
            newPoint = True

            while newPoint:
                p = Point(random.random()*Globals.RESOLUTION[0], random.random()*Globals.RESOLUTION[0])

                newPoint = False

                #Make sure intersections are distenced

                for point in self.intersectionDict:
                    point = Point(point)
                    if abs(point.getX()-p.getX()) < Globals.RESOLUTION[0]/self.maxIntersections/2 or abs(point.getY()-p.getY()) < Globals.RESOLUTION[0]/self.maxIntersections/2:
                        newPoint = True

            self.intersectionDict[tuple(p)]=[]

        for point in self.intersectionDict:
            point = Point(point)
            smallestOrder = []

            while len(smallestOrder)<len(self.intersectionDict)-1:
                highestNumber = float("inf")
                smallestPoint = None
                for otherPoint in self.intersectionDict:
                    otherPoint = Point(otherPoint)
                    if point.getDist(otherPoint)<highestNumber and otherPoint!=point and tuple(otherPoint) not in smallestOrder:
                        smallestPoint = otherPoint
                        highestNumber = point.getDist(otherPoint)

                if smallestPoint:
                    smallestOrder.append(tuple(smallestPoint))

            smallestPointDict[tuple(point)] = smallestOrder

        breakNum = 6

        for i in range(breakNum):
            for point in smallestPointDict:
                if smallestPointDict[point]:
                    otherPoint = smallestPointDict[point][0]
                    if otherPoint not in self.intersectionDict[tuple(point)] and point not in self.intersectionDict[tuple(otherPoint)]:
                        if self.notIntersect([point,otherPoint]):
                            self.intersectionDict[tuple(point)].append(otherPoint)
                            self.intersectionDict[tuple(otherPoint)].append(point)

                    del smallestPointDict[point][0]

        self.roads = []
        alreadyDone =[]
        for point in self.intersectionDict:
            for otherPoint in self.intersectionDict[point]:
                if (otherPoint, point) not in alreadyDone:
                    self.roads.append(Road(start = point, end = otherPoint))
                    alreadyDone.append((point, otherPoint))


    def render(self, renderer):
        self.rects = []
        for point in self.intersectionDict:
            self.rects.append(Rectangle(pos = point, size = [10,10]))
            self.rects[-1].render(renderer)

        for road in self.roads:
            road.render(DisplayDriver.engine)

    def destroy(self):
        for rect in self.rects:
            rect.removeNode()
        for road in self.roads:
            road.removeNode()


class lel():
    def __init__(self):
        self.t = None

    def new(self, event=None):
        if self.t:
            self.t.destroy()
        self.t = Town(maxIntersections=10)
        self.t.render(DisplayDriver.engine)

l = lel()

l.new()
#DisplayDriver.engine.addTask(l.new, [None])
DisplayDriver.eventManager.bind(KEYDOWN, l.new)

#DisplayDriver.engine.addTask(ta)


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

