import math

class Point(list):
    def __init__(self,x,y=None):
        if y!=None:
            list.__init__(self,[x,y])
        else:
            list.__init__(self,x)

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
        ax, ay = self
        bx, by = toPoint
        return math.hypot(bx-ax, by-ay)

    def getPointsList(self):
        return [self[0],self[1]]

    def getX(self):
        return self[0]

    def setX(self,x):
        self[0]=x

    def getY(self):
        return self[1]

    def setY(self,x):
        self[1]=x

    def setPoints(self,x,y):
        self[0]=x
        self[1]=y

    def getPoints(self):
        '''returns new point object'''
        return Point(self[0],self[1])

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

