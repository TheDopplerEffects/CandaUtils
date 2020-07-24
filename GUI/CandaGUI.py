from appJar import gui
from random import randint


class output(object):
    def __init__(self, window, name, canid = 0, fmt = '0|0:64'):
        self.window = window
        self.name = name
        self.mid = canid
        self.fmt = fmt
        
        row = window.gr()
        
        self.window.addEntry('e' + self.name,row,0,0,1)
        self.window.setEntryWidth('e' + self.name, 8)
        self.window.setEntry('e' + self.name,fmt)
        
        self.window.addMeter('m' + self.name,row,1,0,1)
        self.window.setMeter('m' + self.name, 50)
        self.window.setMeterWidth('m' + self.name, 200)
        
        self.window.addLabel('l' + self.name, "0000000000",row,2,0,1)
        self.window.setLabelBg('l' + self.name, "white")
        
    def set(self, value):
        self.window.setLabel('l' + self.name, f'{value:08x}')

def calce():
    for i in range(8):
        for x in range(8):
            p.setLabel(str(i)+str(x), randint(0,1))


p = gui("values")

p.setSticky("nesw")
p.setStretch("row")

p.startScrollPane("LEFT", row=0, column=0, disabled="horizontal")
p.setSticky("enw")
p.setBg("white")
p.setStretch("none")

setLen = 0
newSet(p,i)
setLen = i

p.stopScrollPane()

p.startFrame("R", row=0, column=1)
p.setSticky("nesw")
p.setStretch("both")

for i in range(8):
    for x in range(8):
        p.addLabel(str(i)+str(x), randint(0,1), i,x,1,1)
p.stopFrame()

p.addButton("Calc", calce)
p.go()


