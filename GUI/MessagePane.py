
from appJar import gui

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

p.go()