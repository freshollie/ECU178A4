from DisplayDriver import DisplayDriver
from DisplayDriver.GuiObjects import *
from DisplayDriver.Points import *
from DisplayDriver.Intervals import *
from pygame.locals import *
import random

# Exmaples of how to use DisplayDriver
# None of this is documented on the internet, so if you want to know how to do
# something then you are probably going to have to ask me (Oliver Bell)

#This is designed to run on python 3 but it will work on 2 (Mostly)

RES = [640,480]

# Make an object that inherits an object in GuiObjects

class Robot(Rectangle):
    def __init__(self,pos,size=[20,20]):
        # If you want to centre the rectangle then you have to take into account size
        # Point(pos.getX()-

        Rectangle.__init__(self,pos, size=size, colour=(255,0,0))



class ExampleHelperClass():
    def __init__(self):

        centre = Point(RES[0]/2, RES[1]/2)

        self.r = Robot(centre) # Initialise it

        self.r.render(DisplayDriver.engine) # Render it and it will be displayed on screen

        self.screenText = OnscreenText('', pos=[0,20], size=30)
        self.screenText.render(DisplayDriver.engine)

        self.mouseText = OnscreenText('Mouse is here',size = 20, pos=[-23232,-2323])
        self.mouseText.render(DisplayDriver.engine)

        self.tickCount = 0

        self.counterText = OnscreenText('Tick has been called 0 times',pos = [0,100], size=30)
        self.counterText.render(DisplayDriver.engine)

        DisplayDriver.engine.addTask(self.tick) #Your main function runs on a tick. Called every time the
        # DisplayDriver is going to make a new frame


        # Sequence can be used to perform a task after x seconds

        self.screenText.setText('Waiting 2 seconds')

        Sequence(DisplayDriver.engine, Wait(2),Func(self.startDemo)).start() #WIll perform the sequence once

    def startDemo(self):
        self.rotateLoop = Sequence(DisplayDriver.engine, Func(self.rotateRobot))
        self.moveLoop = Sequence(DisplayDriver.engine, Func(self.newRobotPos), Wait(1))


        Sequence(DisplayDriver.engine,
                 Parrallel( #Parrallel will run 2 functions on the same frame
                     Func(self.rotateLoop.loop),
                     Func(self.screenText.setText,'We can rotate the robot') # You can pass the function arguments too
                 ),
                 Wait(5),
                 Parrallel(
                     Func(self.moveLoop.loop),
                     Func(self.screenText.setText,'And Move it around on the screen')
                 ),
                 Wait(4),
                 Parrallel(
                     Func(self.startInput),
                     Func(self.screenText.setText, 'We can accept keyboard and mouse events')
                 ),
                 Wait(3),
                 Func(self.screenText.setText, '(Move your mouse around the screen)'),
                 Wait(3),
                 Func(self.screenText.setText, '(Press D for a stats window)'),
                 Wait(3),
                 Func(self.screenText.setText, 'Press space to change colours'),
                 Wait(3),
                 Func(self.screenText.setText, 'Press escape to quit')
            ).start()

    def rotateRobot(self):
        self.r.setRotation(self.r.getRotation()+10)

    def newRobotPos(self):
        self.r.setPos(Point(random.random()*RES[0],random.random()*RES[1]))

    def mouseEvent(self, event):
        self.mouseText.setPos(event.pos)

    def keyboardEvent(self, event):
        if event.key == K_SPACE: # Space key is pressed
            self.changeColour()
        elif event.key == K_ESCAPE: # Escape key pressed
            DisplayDriver.engine.stop()

    def changeColour(self):
        self.r.setColour([random.random()*255,random.random()*255,random.random()*255])

    def startInput(self):
        DisplayDriver.eventManager.bind(MOUSEMOTION, self.mouseEvent) # This will bind the mouse motion to any
        DisplayDriver.eventManager.bind(KEYDOWN, self.keyboardEvent)

    def tick(self):
        # Do something every new frame
        self.tickCount+=1
        self.counterText.setText('Tick has been called %s times' %(self.tickCount))

ExampleHelperClass()

DisplayDriver.engine.setFrameRate(50)
DisplayDriver.engine.graphics.setRes(RES)

DisplayDriver.init() # Start the display driver




