from DisplayDriver import DisplayDriver
import sys
import random
import time
from DisplayDriver.Intervals import *
from DisplayDriver.GuiObjects import *
from pygame.locals import *
DisplayDriver.engine.setFrameRate(50)
DisplayDriver.engine.graphics.setBackground(BLACK)


# Some more examples of using DisplayDriver to make a fireworks show.
# Not really commented so I guess you will just have to work this one out.

res=[640,480]

class Bang:
    def __init__(self,engine,pos=[res[0]/2,res[1]/2],size=20,depth=0,maxDepth=2):
        self.maxDepth=maxDepth
        self.engine=engine
        self.items=[]
        for i in range(size):
            self.items.append(Rectangle(pos,[random.randint(1,3),random.randint(1,3)],border=0,
                                        colour=(random.randint(10,255),
                                                random.randint(10,255),
                                                random.randint(10,255))))
        
        for item in self.items:
            #taskId=DisplayDriver.engine.addTask(count.tick)
            xPlus=random.choice([-1,1])*random.random()*random.randint(1,10)
            yPlus=random.choice([-1,1])*random.random()*random.randint(1,10)
            x=item.getPos()[0]
            y=item.getPos()[1]
            seq=Sequence(engine)
            seq.append(Func(item.render,engine))
            
            for i in range(random.randint(10,30)):
                seq.append(Func(item.setPos,[x+(xPlus*i),y+(yPlus*i)]))
                xPlus*=0.981
                yPlus*=0.981
            #seq.append(Func(DisplayDriver.engine.removeTask,taskId))
            if not random.randint(1,1):
                seq.append(Func(self.makeBang,[x+(xPlus*i),y+(yPlus*i)],depth))
            seq.append(Func(item.removeNode))
            seq.start()

    def makeBang(self,pos,depth):
        if depth<self.maxDepth:
            depth+=1
            Bang(self.engine,pos,size=random.randint(1,20),depth=depth)


def doBang(event):
    Bang(DisplayDriver.engine,event.pos,size=random.randint(10,50)) # Change these numbers to make a larger explosion



DisplayDriver.eventManager.bind(MOUSEBUTTONDOWN,doBang)
DisplayDriver.debugger.toggle()
DisplayDriver.engine.graphics.setRes(res)


DisplayDriver.init()
