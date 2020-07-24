from appJar import gui
from random import randint


def newSet(frame,num):
    row = frame.gr()
    frame.addEntry('e' + str(num),row,0,0,1)
    frame.addMeter('m' + str(num),row,1,0,1)
    frame.addLabel('l' + str(num), "0000000000",row,2,0,1)
    frame.setLabelBg('l' + str(num), "white")
    frame.setEntryWidth('e' + str(num), 8)
    frame.setMeter('m' + str(num), 50)
    frame.setMeterWidth('m' + str(num), 200)
    frame.setEntry('e' + str(num),"0|0:64")

def calce():
    for i in range(8):
        for x in range(8):
            p.setLabel(str(i)+str(x), randint(0,1))


p = gui("values")

p.setSticky("nesw")
p.setStretch("row")

p.startScrollPane("LEFT", row=0, column=0, disabled="horizontal")
p.setSticky("enw")
p.setBg("black")
p.setStretch("none")

setLen = 0
for i in range(15):
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

p.addButton("Calc", calce
p.go()


