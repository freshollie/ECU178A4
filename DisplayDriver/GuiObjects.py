from .Intervals import *
from .Globals import *
from .Points import *
import pygame
import threading
import time
import math
pygame.font.init()            

class GuiObjectBase(object):
    '''
    At the base of all object represented
    on screem, has methods that the
    DisplayDriver needs to render the object.

    A notable method that is to be defined by the user,
    '''
    def __init__(self,pos=Point(0,0),rotation=0):
        '''
        Initalises the GuiObject
        '''
        self.pos=Point(pos)
        self.rotation=rotation
        self.hidden=False
        self.rendered=None
        self.angle=rotation

    def hide(self):
        '''
        Set the DisplayDriver to not
        render this object without removing
        it from the pool.

        Used if you only want to temporerally hide
        something
        '''
        self.hidden=True

    def show(self):
        '''
        Set the DisplayDriver to render this
        object again.

        Will not work unless the object is
        already rendered but hidden
        '''
        self.hidden=False

    def setPos(self,pos):
        '''
        Set the position of the object on the screen.

        The position works from the top left pixel being 0,0
        just like pygame.

        The position can be a list or a Point object.
        '''
        
        self.pos=Point(pos)

    def getPos(self):
        '''
        Returns the objects screen position
        '''
        return self.pos.getPoints()

    def setRotation(self,angle):
        '''
        Sets the rotation of the object
        '''
        self.rotation=angle

    def getRotation(self):
        '''
        Gets the rotation of the object
        '''
        return self.rotation

    def setX(self,x):
        '''
        Sets the objects X Value
        '''
        self.pos,setX(x)

    def setY(self,y):
        '''
        Sets the objects Y Value
        '''
        self.pos.setY(y)

    def getX(self):
        '''
        Sets the objects X value
        '''
        
        return self.pos.getX()

    def getY(self):
        '''
        Gets the objects Y value
        '''
        
        return self.pos.getY()

    def draw(self):
        raise(SyntaxError("Missing draw method from object, don't know how to draw object"))

    def render(self,core):
        '''
        Add the object to the DisplayDrivers
        rendering pool
        '''
        core.graphics.addEntity(self)
        self.rendered=core

    def removeNode(self):
        '''
        Remove the object from the render pool
        '''
        if self.rendered:
            self.rendered.graphics.removeEntity(self)
            self.rendered=None

class Image(GuiObjectBase):
    '''
    Image object to render an object on screen
    '''
    
    def __init__(self,pos,image,rotation=0):
        GuiObjectBase.__init__(self,pos,rotation)
        self.image=image

    def draw(self,screen):
        '''
        Draws the image on screen
        '''
        screen.blit(self.image,self.pos)

class OnscreenText(GuiObjectBase):
    '''
    Object to represent text on screen as
    an object with position and rotation
    '''
    
    def __init__(self,text='',pos=[0,0],size=12,fontName=None,font=None,colour=BLACK):
        '''
        Initialise the object
        '''
        GuiObjectBase.__init__(self,pos=pos)
        self.colour=colour
        self.font=font
        self.size=size
        self.fontName=fontName
        if not font:
            self.genFont()
        self.setText(text)

    def genFont(self):
        self.font=pygame.font.Font(self.fontName, self.size)

    def setText(self,text):
        '''
        Sets the text of the object
        '''
        self.text=text
        self.renderedText=self.font.render(self.text,1,self.colour)
        
    def draw(self,screen):
        '''
        Called by DisplayDriver to draw the object
        '''
        image=pygame.transform.rotate(self.renderedText,-self.rotation)
        image.get_rect().center=self.pos
        screen.blit(image,self.pos) #Render text

class Polygon(GuiObjectBase):
    '''
    Polygon object creates a shape with
    as many points as needed, and renders
    that object
    '''
    def __init__(self,pos,points=[],colour=BLACK,border=0):
        '''
        Initialise the Polygon
        '''
        GuiObjectBase.__init__(self,pos)
        self.colour=colour
        self.border=border
        if points:
            self.newPoints(points)
        else:
            self.points=[]

    def translatePoints(self,differenceX,differenceY):
        '''
        Move all points by differenceX and differenceY
        '''
        points=[]
        for item in self.points:
            points.append(Point(item[0]+differenceX,item[1]+differenceY))
        self.setPoints(points)
        self.pos=Point(self.pos[0]+differenceX,self.pos[1]+differenceY)

    def setPos(self,pos):
        '''
        Sets the new pos of the polygon
        '''
        differenceX=pos[0]-self.pos[0]
        differenceY=pos[1]-self.pos[1]

        self.translatePoints(differenceX,differenceY)

    def newPoints(self,points):
        '''
        Set the new points of the polygon
        '''
        
        self.setPoints(points)
        image = pygame.draw.polygon(pygame.Surface(RES),self.colour,self.points,self.border)
        self.pos=Point(image.center)

    def setColour(self,colour):
        '''
        Set the colour of the polygon
        '''
        self.colour=colour

    def setBorder(self,border):
        '''
        Set if a boarder should be rendered
        on the Polygon
        '''
        self.border=border
        
    def setPoints(self,points):
        '''
        Sets the points
        '''
        self.points=points[:]

    def getPoints(self):
        '''
        Returns the points
        '''
        return self.points[:]

    def setRotation(self,angle):
        self.rotation = angle
        self.setAngle(angle)

    def setAngle(self,angle):
        '''
        Sets the angle of the polygon
        '''
        while angle>=360:
            angle-=360
        while angle<0:
            angle+=360
        angleDifference=angle-self.angle
        self.angle=angle
        self.rotatePoints(angleDifference)

    def rotatePoints(self,theta):
        '''
            Rotates all points about the centre point
            by theta
        '''
        points=[]
        for point in self.points:
            points.append(point.rotPoint(self.pos,theta))
        self.setPoints(points)
        
    def draw(self,screen):
        '''
	        Draws the polygon
        '''
        if self.points:
            pygame.draw.polygon(screen,self.colour,self.points,self.border)
            
class Rectangle(Polygon):
    '''
    An extension of polygon designed to draw a rectangle
    of specific size
    '''

    def __init__(self,pos,size,colour=BLACK,border=0,centered=True):
        '''
        Initialise the rectangle
        '''
        self.size=size
        self.centered=centered
        self.pos=pos
        Polygon.__init__(self,pos,points=self.makePoints(),colour=colour,border=border)

    def setSize(self,size):
        '''
        Set the size of the rectangle
        '''
        self.size=size[:]

    def makePoints(self):
        '''
        Return all the generated corner points
        '''
        if self.centered:
            return [Point(self.pos[0]-self.size[0]/2,self.pos[1]-self.size[1]/2),
                    Point(self.pos[0]+self.size[0]/2,self.pos[1]-self.size[1]/2),
                    Point(self.pos[0]+self.size[0]/2,self.pos[1]+self.size[1]/2),
                    Point(self.pos[0]-self.size[0]/2,self.pos[1]+self.size[1]/2)
                    ]
        else:
            return [Point(self.pos),
                    Point(self.pos[0]+self.size[0], self.pos[1]),
                    Point(self.pos[0]+self.size[0], self.pos[1]+self.size[1]),
                    Point(self.pos[0], self.pos[1]+self.size[1])
                    ]

 
class Border(Rectangle):
    '''
    Extends rectangle but only renders the board
    of the rectangle
    '''

    def __init__(self,pos,size,colour=BLACK,border=2):
        if not border:
            border=1
        Rectangle.__init__(self,pos,size,colour,border)
        
        

class TextBox(object):
    '''
    Textbox is a helper object that congrigates
    rectangle as background and OnscreenText objects
    to a textbox
    '''

    def __init__(self,pos,size,fontSize=12,backgroundColour=WHITE,borderColour=BLACK,border=2):
        '''
        Initialise the textbox
        '''
        if border:
            self.border=Border(pos,size,borderColour,border)
        else:
            self.border=None
        self.background=Rectangle(pos,size,backgroundColour,0)
        self.size=size
        self.text=[]
        self.pos=pos[:]
        

    def setText(self,text,startLine=0):
        '''
        Set the text of the box and wrap it in the box
        '''
        for i in range(startLine,self.size[0]):
            if len(line)>self.size[0]-2:
                if line[24]==" ":
                    self.text[i].setText([line[:24]])
                    line=line[24:]
                    
                else:
                    for x in range(25,0,-1):
                        if line[x-1]==" ":
                            self.text[i].setText([line[:x-1]])
                            line=line[x-1:]
                            break
            else:
                self.text[i].setText([line])
                break

    def setLine(self,line,text,wrap=False):
        '''
        Set a specific line of a textbox
        '''
        if len(text)>self.size[0]-2:
            if wrap:
                self.setText(text,line)
            else:
                text=text[:self.size[0]-2]
        self.text[line].setText([text])

    def render(self,renderer):
        '''
        Render the element of the text box
        '''
        self.background.render(renderer)
        self.border.render(renderer)
        for text in self.text:
            text.render(renderer)

    def removeNode(self):
        '''
        Remove the elements of the textbox from the render
        pool
        '''
        self.background.removeNode()
        self.border.removeNode()
        for text in self.text:
            text.removeNode()

    def hide(self):
        '''
        Hide the elements of the textbox
        '''
        self.background.hide()
        self.border.hide()
        for text in self.text:
            text.hide()
        

    def show(self):
        '''
        Show the elements of the textbox
        '''
        self.background.show()
        self.border.show()
        for text in self.text:
            text.show()

    def setPos(self,pos):
        '''
        Set the positions of the elements
        '''
        self.background.setPos(pos)
        self.border.setPos(pos)

        for text in self.text:
            for i in range(len(self.text)):
                self.text.setPos([self.pos[0]+1,self.pos[1]+i+1])
    
        
    
    
        
