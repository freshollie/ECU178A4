import math

class Point(object):
    def __init__(self,x,y=None):
        if y!=None:
            self.x = x
            self.y = y
        else:
            self.x = x[0]
            self.y = x[1]

        #list.__init__(self, [self.x, self.y])

    def rotPoint(self,axisPoint,ang):
        """
        Rotates a point around another centerPoint. Angle is in degrees.
        Rotation is counter-clockwise
        """
        point, centerPoint, angle = self, axisPoint, ang
        angle = math.radians(angle)
        temp_point = point[0]-centerPoint[0] , point[1]-centerPoint[1]
        temp_point = ( temp_point[0]*math.cos(angle)-temp_point[1]*math.sin(angle) , temp_point[0]*math.sin(angle)+temp_point[1]*math.cos(angle))
        temp_point = temp_point[0]+centerPoint[0] , temp_point[1]+centerPoint[1]
        
        return Point(temp_point[0],temp_point[1])

    def getBearing(self,about):
        angle = math.degrees(
                math.atan2(self.getY() - about.getY(),
                           self.getX() - about.getX())
                )
        bearing = (angle + 90) % 360
        return bearing

    def getDist(self,toPoint):
        if hasattr(toPoint, '__iter__'):
            ax, ay = self.getPointsList()
            bx, by = toPoint
            return math.hypot(bx-ax, by-ay)
        else:
            raise(TypeError("topoint must be an iterable"))

    def getPointsList(self):
        return [self.x,self.y]

    def getX(self):
        return self.x

    def setX(self,x):
        self.x = x

    def getY(self):
        return self.y

    def setY(self,y):
        self.y = y

    def setPoints(self,x,y):
        self.y = y
        self.x = x

    def getPoints(self):
        '''returns new point object'''
        return Point(self.x, self.y)

    def getCenter(self,angle,radius):
        '''Returns a center point of circle from the point
           the radius of the circle and the angle that the point is at
        '''
        x=self.getX()+(radius*math.cos(math.radians(angle)))
        y=self.getY()+(radius*math.sin(math.radians(angle)))
        return Point(x,y)

    def getDistance(self,point):
        '''
           Gets the distance between its self and the input point
        '''
        return math.sqrt((point.getY()-self.getY())**2+(point.getX()-self.getX())**2)

    def __eq__(self, other):
        #print(other)
        if isinstance(other, Point):
            return other.getPointsList()==self.getPointsList()
        else:
            return other == self.getPointsList()

    def __getitem__(self, i):
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise(IndexError())

    def __iter__(self):
        return iter(self.getPointsList())

    def __len__(self):
        return 2

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str([self.x, self.y])