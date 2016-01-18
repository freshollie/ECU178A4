import time
import sys
import os
from .Globals import *
from .Points import *
from .GuiObjects import *
from pygame.locals import *

class Debug(object):
    def __init__(self,engine,pos=Point(0,0),background=BLACK,textColour=WHITE):
        self.count=0
        self.taskId=None
        self.toggled=True
        self.rect=Rectangle(pos, [170,80], colour=background, border=0, centered = False )
        self.text=[]
        for i in range(5):
            self.text.append(OnscreenText('',Point(pos[0],pos[1]+(i*13)),colour=textColour,size=20))
            
        self.engine=engine
        self.startTime=time.time()

    def start(self):
        if not self.timeSeq.started:
            self.timeSeq.loop()

    def stop(self):
        #self.timeSeq.finish()
        pass

    def tick(self):
        if self.toggled:
            self.text[0].setText('Fps: %s' %(self.engine.fpsClock.get_fps()))
            self.text[1].setText('Entitys: %s' %(len(self.engine.graphics.entityList)))
            self.text[2].setText('Tasks/frame: %s' %(len(self.engine.taskDict)))
            self.text[3].setText('Real time: %s' %(datetime.timedelta(seconds=time.time()-self.startTime)))

    def tick2(self):
        self.text[4].setText('Program time: %s' %(datetime.timedelta(seconds=self.count)))
        self.count+=1

    def render(self,engine):
        self.rect.render(engine)
        self.timeSeq=Sequence(engine,
                              Func(self.tick2),
                              Wait(1)
                             )
        
        for text in self.text:
            text.render(engine)
            
        if not self.timeSeq.started:
            self.timeSeq.loop()

    def show(self):
        self.rect.show()
        for text in self.text:
            text.show()

    def hide(self):
        self.rect.hide()
        for text in self.text:
            text.hide()

    def toggle(self):
        if self.toggled:
            self.hide()
            self.stop()
            self.toggled=False
        else:
            self.show()
            self.start()
            self.toggled=True

    def doEvent(self,event):
        if event.key==K_d:
            self.toggle()
            
    def destroy(self):
        self.rect.removeNode()
        for text in self.text:
            text.removeNode()

class StickerManager():
    def __init__(self):
        pass

    def tick(self):
        pass
