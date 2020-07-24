from appJar import gui
from random import randint
from time import sleep
from random import randint

class output(object):
    def __init__(self, window, name, canid = 0, fmt = '0|0:64'):
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
        self.window.setMeterWidth('m' + self.name, 200)
        
        self.window.addLabel('l' + self.name, "0000000000",row,2,0,1)
        self.window.setLabelBg('l' + self.name, "white")
        self.window.stopScrollPane()
        
    def set(self, value):
        self.window.setLabel('l' + self.name, f'{value:08x}')

def new():
    name = p.getEntry('name')
    mid = p.getEntry('mid')
    fmt = p.getEntry('fmt')
    outputs.append(output(p,name, mid, fmt))
    
def simulater():
    while 1:
        sleep(1)
        for i in outputs:
            num = randint(0,0xffffffff)
            p.queueFunction(i.set ,num)
        

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
p.addButton("Make Value", new, 0,3)

p.stopFrame()

p.thread(simulater)

p.go()


