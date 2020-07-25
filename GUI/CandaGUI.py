from appJar import gui
from random import randint
import time as t
from random import randint
from panda import Panda

UPDATE_FREQUINCY = 10 #hz

def formatBits(num, fmt): #!!!!!!! replace this with a proper module in CandaUtils
    
    start,size,*mod = fmt.split(':')
    if fmt == '':
        return num	
    return num>>int(start) & int(''.rjust(int(size), '1'),2)

class output(object):
    def __init__(self, window: gui, name, canid = 0, fmt = '0|0:64'):
        self.window = window
        self.name = name
        self.mid = canid
        self.fmt = fmt
        

        self.window.openScrollPane('left')
        
        row = self.window.gr()
        
        self.window.addEntry('e' + self.name,row,0,0,1)
        self.window.setEntryWidth('e' + self.name, 8)
        self.window.setEntry('e' + self.name,fmt)
        
        self.window.addMeter('m' + self.name,row,1,0,1)
        self.window.setMeter('m' + self.name, 50)
        self.window.setMeterFill('m' + self.name, "red")
        self.window.setMeterWidth('m' + self.name, 200)
        
        self.window.addLabel('l' + self.name, "0000000000000000",row,2,0,1)
        self.window.setLabelBg('l' + self.name, "white")
        self.window.setLabelAlign('l' + self.name, "right")
        self.window.setLabelWidth('l' + self.name, 16)
        self.window.getLabelWidget('l' + self.name).config(font=("Courier New", 13))        
        #Courier New
        self.window.stopScrollPane()
        
    def set(self, value):
        self.window.setLabel('l' + self.name, f'{formatBits(value, self.fmt):x}')  #remove formmatting remporarly
        #self.window.setMeter('m' + self.name, (value / 0xffffffffffffffff) * 100)
        
def new():
    name = p.getEntry('name')
    mid = int(p.getEntry('mid'), 16)
    fmt = p.getEntry('fmt')
    outputs.append(output(p,name, mid, fmt))


def distrobuteData(dataBuffer):
    for MID, _, data, bus in dataBuffer:
        for d in outputs: #Data Distrobution betwean the output lines
            if d.mid == MID:
                d.set(data)
                
def connectPanda():
    p.showSubWindow("con")
    t.sleep(2)
    try:
        dev = Panda()
    except:
        p.setLabel("ConnectStatus", "FAILED! Trying to connect to panda over Wifi")      
        try:
            print('Trying panda')
            assert False  #!!!!!!!!!!!!!panda wifi donsn't timout
            dev = Panda("WIFI")
        except:
            p.setLabel("ConnectStatus", "Connection timed out!\nClosing in 3 seconds")
            t.sleep(3)
            p.thread(simulater) 
            #app.stop()
            #sys.exit(0)
    p.destroySubWindow('con')
                   
    
    
            
            
        
        
def simulater():
    ids = [0x120, 0x0e10]
    while 1:
        start = t.time()
        buffer = []
        for o in range(1000):
            buffer.append((ids[randint(0, 1)], None, (randint(0,0xffffffffffff)<<16)+ 0x8000 + randint(0,0x7fff), 8)) #get data
        p.queueFunction(distrobuteData(buffer))
        t.sleep(max((1/UPDATE_FREQUINCY)-(t.time() - start), 0))     
        
def runCan():
    while 1:

        start = t.time()        
        can_recv = p.can_recv()
        p.queueFunction(distrobuteData(buffer))
        t.sleep(max((1/UPDATE_FREQUINCY)-(t.time() - start), 0))          
        

        

p = gui("values")

p.setSticky("nesw")
p.setStretch("row")

p.startScrollPane("left", row=0, column=0, disabled="horizontal")

p.setSticky("enw")
p.setBg("white")
p.setStretch("none")

p.addLabel('FM', "Format",0,0)
p.addLabel('ME', "Meter",0,1)
p.addLabel('OT', "Value",0,2)
p.stopScrollPane()

p.startFrame("R", row=0, column=1)

p.setSticky("nesw")
p.setStretch("both")
for i in range(8):
    for x in range(8):
        p.addLabel(str(i)+str(x), randint(0,1), i,x,1,1)
        
p.stopFrame()

outputs = []
p.startFrame('bottom', row=1, colspan=2)

p.addLabelEntry("name", 0,0)
p.addLabelEntry("mid", 0,1)
p.addLabelEntry("fmt", 0,2)
p.setEntry("name", 'Test')
p.setEntry("mid", '0e1e')
p.setEntry("fmt", "0:64")
new()
p.addButton("Make Value", new, 0,3)

p.stopFrame()

p.startSubWindow("con")
p.addLabel("ConnectStatus", "Connecting: USB") 
p.stopSubWindow()   

#p.thread(simulater)

p.setStartFunction(connectPanda)
p.go()


