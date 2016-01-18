import datetime

class Sequence(dict):
    
    def __init__(self,engine,*intervals):
        self.started=False
        self.engine=engine
        self.name=''
        self['sequence']=[]
        for interval in intervals:
            self['sequence'].append(interval)

    def append(self,interval):
        self['sequence'].append(interval)

    def start(self):
        if not self.started:
            if 'loop' in self:
                del self['loop']
            self.started=True
            self.engine.addSequence(self)

    def loop(self):
        if not self.started:
            self['loop']=True
            self.started=True
            self.engine.addSequence(self)

    def finish(self):
        if self.started and 'funcNum' in self:
            self['funcNum']=len(self['sequence'])+1

    def printStructure(self):
        print('Sequence object %s Running:' %(self.started))
        indent=0
        time=0
        for object in self['sequence']:
            if type(object)==Wait:
                print('|%s: %s Wait(%s)' %(datetime.timedelta(seconds=time),
                                           indent*'    ',
                                           object['wait']
                                           )
                      )
                time+=object['wait']
                
            elif type(object)==Func:
                line1='|%s:%s Function{' %(datetime.timedelta(seconds=time),
                                               indent*'    '
                                            )
                line2='%s%s(%s)' %(len(line1)*' ',
                                   object['function'][0].__name__,
                                   ('\n'+len(line1)*' '+',').join([str(item) for item in object['function'][0:]])
                                   )
                line3='%s}' %(len(line1)*' ')
                print(line1)
                print(line2)
                print(line3)
                
                
            
            
    def __str__(self):
        self.printStructure()
        return ''

class Func(dict):

    def __init__(self,function,*args):
        self['function']=[function,args]
        
    def __str__(self):
        return 'Function Interval %s' %self['function'][0].__name__

class Wait(dict):

    def __init__(self,time):
        self['wait']=time

    def __str__(self):
        return 'Wait Interval %s' %self['wait']

class Parrallel(dict):

    def __init__(self,*intervals):
        self['parrallel']=[]
        for interval in intervals:
            self['parrallel'].append(interval)

    def __str__(self):
        return 'Parrallel interval %s' %([function.__name__ for function in self['parrallel']])


