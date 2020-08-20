
from appJar import gui
from random import randint

currentMessage = None #stores active message window
messagedict = {}

class messageWindow():
    def __init__(self, window: gui, name:str, address:int, ):
        self.window = window
        self.name = name
        self.address = address
        self.signals = {}

        self.window.openScrollPane('MessagePane')
        nextRow = self.window.gr()

        #Message select
        self.window.addRadioButton("messageSelect", name)
        self.window.setRadioButtonChangeFunction('messageSelect', SelectMessageEvent)

        #Message MID label
        self.window.addLabel('Address' + self.name, address, nextRow,1,0,1)
        self.window.setLabelWidth('Address' + self.name, 5)

        #Message value
        self.messageValueLabel = self.window.addLabel('Value' + self.name, "FFFFFFFFFFFFFFFF",nextRow,2,)

        #Signals frame
        self.window.setPadding((20,0))
        self.window.startFrame("SigFrame"+self.name, row=nextRow+1, column=0, colspan=4)
        self.window.setBg('yellow')
        self.signals['New_Signal'] = SignalOut(self.window, self.name+'New_Signal', 'New_Signal')
        self.window.stopFrame()
        self.window.setPadding((0,0))

        self.window.stopScrollPane()

    def set(self, value):
        self.messageValueLabel.config(text=str(value))
        for i in self.signals.values():
            i.set(value)

    def addSignal(self, name): 
        self.window.openFrame("SigFrame"+self.name)
        #self.window.setPadding((20,0))
        self.signals[name] = SignalOut(self.window, self.name+name, name) #Do i really need a class to manage signals?
        self.window.stopFrame()

class SignalOut():
    def __init__(self, window, id, name):
        self.name = name
        self.id = id
        self.window = window
        
        nextRow = self.window.gr()
        
        self.window.addLabel('signalName' + self.id, name, nextRow,0,0,1)

        self.SignalValueLabel = self.window.addLabel('signalValue' + self.id, "FFFFFFFFFFFFFFFF",nextRow,2,0,1)
        self.window.setLabelAlign('signalValue' + self.id, "right")
        self.window.setLabelWidth('signalValue' + self.id, 16)
        self.window.getLabelWidget('signalValue' + self.id).config(font=("Courier New", 13))  
        
    def set(self, value):
        self.SignalValueLabel.config(text=value, )



def press(val):
    messageName = ''
    messagedict['test2'] = messageWindow(p, 'test2', 110)

def SelectMessageEvent():
    global currentMessage
    b = p.getRadioButton('messageSelect')
    currentMessage = messagedict[b]

def randout():
    global currentMessage
    currentMessage.set(str(randint(0, 0xFFFFFFFFFFFFFFFF)))

def addSignal(name = 'New_Signal'):
    global currentMessage
    currentMessage.addSignal(name)



with gui("values") as p:
    p.setSize(500, 300)
    p.setSticky("nesw")
    p.setStretch("column")

    p.startScrollPane("MessagePane", row=0, column=0, colspan=3, disabled="horizontal")
    p.setSticky("enw")
    p.setBg("white")
    p.setStretch("none")
    p.addLabel('FM', "Message Name",0,0)
    p.addLabel('ME', "MID",0,1)
    p.addLabel('OT', "Value",0,2)
    p.stopScrollPane()
    
    p.addButton("new message", press, row=1, column=0)
    p.addButton("new signal", addSignal, row=1, column=1)
    p.addButton("rand output", randout, row=1, column=2)

    currentMessage = messageWindow(p, 'test', 110)
    messagedict['test'] = currentMessage


