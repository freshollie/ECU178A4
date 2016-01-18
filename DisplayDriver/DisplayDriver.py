# Converted ascii display driver to
# Run pygame
import time
import sys
import os
from . import Debug
from .Intervals import *
from .Points import *
from pygame.locals import *
from .EventManager import *
from .GuiObjects import *

class Graphics(object):
    '''
    Graphics is graphical driver for the engine. It makes the display
    and manages the enities.
    '''
    
    def __init__(self,resolution=RES):
        '''
        The initialisation contains some properties of the engine
        '''
        self.screen=pygame.display.set_mode(resolution)
        self.entityList=[] # Creates an empty entity list
        self.axis2index={'x':0,'y':1} # Unused
        self.backgroundLetter=' ' # Setting what the background will look like
        self.hiddenEntitys=[] # Setting the list of entities that are hidden
        self.background=WHITE
                            
        self.lastDisplay=[] # Used to check if the display is exactly the same as
                            # the last display to see if it needs to print the display
        
                            

    def createBlankDisplay(self):
        '''
        Creates a blank display that the createDisplay method can
        over right to make the display.
        '''
        if type(self.background)==tuple or type(self.background)==list:
            self.screen.fill(self.background)
        else:
            self.screen.fill(WHITE)
            self.screen.blit(self.background,[0,0])

    def createDisplay(self):
        '''
        Creates a new display
        '''
        self.createBlankDisplay()
        for entity in self.entityList:
            if not entity.hidden:
                entity.draw(self.screen)
            
    def addEntity(self,object):
        '''
        When an entity is rendered it is added to the entity
        list of the graphics engine which means that the
        graphics engine has a reference to that object so
        it can get key things from it like its position and
        image
        '''
        
        self.entityList.append(object) # Add the object to the list of entitys

    def removeEntity(self,object):
        '''
        To remove and entity it needs to be added to a remove
        list so that it doesn't get removed while the create
        display method is iterating
        '''
        
        self.entityList.remove(object) #Delete the object from the entity render list

    def printDisplay(self):
        '''
        Print display is the output of the graphics engine
        it is run after a display has been created to print
        the frame
        '''

        pygame.display.flip()

    def setRes(self,resolution):
        '''
        Set the resolution of the graphics engine
        '''
        
        self.screen=pygame.display.set_mode(resolution)

    def setBackground(self,image):
        '''
        Set the background, can be an image or a colour
        tuple
        '''
        self.background=image
            

class Core(object):
    '''
    Core is the main display driver. It runs the Display and manages the tasks.
    '''
    
    def __init__(self,frameRate=12,name='Game'):
        '''
        Initialise display Driver
        '''
        self.graphics=Graphics() # Define the graphical object
        self.fpsClock=pygame.time.Clock()
        self.name=name  # Set the name of the Display Driver
        self.frameNum=0 # Set the frame number it it on to 0
        self.taskDict={} # Setting the task dict to empty
        self.quedSequences=[] # Setting the qued sequence list to empty
        self.quedTasks=[] # Setting the quest task list to empty
        self.startTime=time.time()
        
        self.runOnceList=[] # Setting the run once list to empty
        self.sequences=[] # Setting the list of sequences to empty
        self.running=False # Used to signify if the display driver is running so that the thread can end
        self.setFrameRate(frameRate)
        self.maxTaskValue=0 # maxTaskValue is used to give a task a designated number
        self.timeTaken=1 # Defined incase it is rederence before the main loop has started
        self.removedTasks=[] # Setting the removed last list to empty
        self.addedTasks={} # Setting the added task dict to empty
        self.seconds=0 # Used in debug for run time
        self.minutes=0 # Used in debug for run time
        self.hours=0 # Used in debug for run time
        self.days=0 # Used in debug for run time
        self.threadPrint=False # Used to set if to thread the print display (for higher fps)

    def setFrameRate(self,frameRate):
        '''
        Set a new framerate if the user would like their own tick rate
        but a slower tick rate is recomended for a less flickery experience
        '''

        self.frameRate=frameRate
        self.frameLength=1.0/frameRate

    def addTask(self,task,arguments=[],once=False):
        '''
        Adding a task to the engine is the only way to interact with
        the graphics engine and the display driver. When a task has
        been added, every frame the tasks will be run.
        '''

        maxTaskValue=self.maxTaskValue # Make a copy of the max task value
        i=0
        while True: # So you can have infinate tasks
            if str(i) not in self.taskDict: # Check that the task key has not already been used
                maxTaskValue=i # Set the max task value to that value
                break # Break out of the while loop
            i+=1
        self.taskDict[str(maxTaskValue)]=[task,arguments]
        if once:
            self.runOnceList.append(str(maxTaskValue))
        self.maxTaskValue=maxTaskValue
        return str(maxTaskValue)

    def removeTask(self,taskValue):
        '''
        Removes task from task pool
        '''
        self.removedTasks.append(taskValue)

    def removeUnneededTasks(self):
        '''
        Remove undeeded tasks from task pool
        '''
        for taskValue in self.runOnceList:
            del self.taskDict[taskValue]
        self.runOnceList=[]
    
    def mainLoop(self):
        '''
        Runs the mainloop of the engine
        '''
        while self.running:
            self.checkSequences()
            self.tick()
            self.graphics.createDisplay()
            self.graphics.printDisplay()
            self.removeUnneededTasks()
            self.fpsClock.tick(self.frameRate)
            
        pygame.quit()

    def addSequence(self,sequence):
        '''
        Add a sequence to run
        '''
        self.sequences.append(sequence)
        self.sequences[-1]['funcNum']=-1

    def deleteSequence(self,sequence):
        '''
        Remove a sequence
        '''
        self.sequences.remove(sequence)

    def checkSequences(self):
        '''
        Checks sequences and adds their tasks to the task
        pool when they need to be executed
        '''
        
        for sequence in self.sequences:
            if sequence['funcNum']+1==len(sequence['sequence']):
                if 'loop' not in sequence:
                    self.deleteSequence(sequence)
                    continue
                
                elif not sequence['loop']:
                    self.deleteSequence(sequence)
                    continue
                
                else:
                    if sequence['loop']==True:
                        sequence['funcNum']=-1
                    else:
                        sequence['loop']-=1
                        sequence['funcNum']=-1
                        
                    
            sequence['funcNum']+=1
            sequenceItem=sequence['sequence'][sequence['funcNum']]
            
            if 'function' in sequenceItem:
                self.addTask(sequenceItem['function'][0],sequenceItem['function'][1],once=True)
                
            elif 'parrallel' in sequenceItem:
                for function in sequenceItem['parrallel']:
                    self.addTask(function['function'][0],function['function'][1],once=True)
                    
            elif 'wait' in sequenceItem:
                loopNum=int(sequenceItem['wait']/self.frameLength)-2
                if loopNum<0:
                    loopNum=0
                sequence['sequence'][sequence['funcNum']]={'ignore':0}
                for i in range(int(loopNum)):
                    sequence['sequence'].insert(sequence['funcNum']+1,{'ignore':0})
            else:
                continue
                
    def tick(self):
        '''
        Called every frame, will perform every task
        that needs to be performed.
        '''
        self.frameNum+=1
        for key in self.removedTasks:
            del self.taskDict[key]
        taskDict=self.taskDict.copy()
        self.removedTasks=[]
        for taskKey in taskDict:
            self.doTask(taskDict[taskKey][0],taskDict[taskKey][1])
            
    def doTask(self,function,arguments,**kwds):
        '''
        Performs the specific function with arguments
        and keyword arguments
        '''
        function(*arguments,**kwds)
    
    def start(self):
        '''
        Start the engine
        '''
        self.running=True
        self.beforeTime=time.time()
        self.mainLoop()

    def stop(self,event):
        '''
        Sets the engine to stop
        '''
        print('End')
        self.running=False
        

engine=Core()
debugger=Debug.Debug(engine)

eventManager=EventManager(pygame)

eventManager.bind(KEYDOWN,debugger.doEvent)
eventManager.bind(QUIT,engine.stop)

engine.addTask(eventManager.tick)
engine.addTask(debugger.tick)

debugger.render(engine=engine)
debugger.toggle()

stickerManager=Debug.StickerManager()

def init():
    '''
    Starts DisplayDriver and initialises pygame,
    can be called after all tasks have been
    added to DisplayDriver so that they are ready
    to upon startup
    '''
        
    pygame.init()
    engine.start()
