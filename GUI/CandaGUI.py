from appJar import gui
from random import randint
import time as t
#from panda import Panda
import struct 

DEBUG = 0
UPDATE_FREQUINCY = 10 #hz




#inject custom methods to panda
def parse_can_bufferNEW(dat, addresses = None):
    ret = []
    for j in range(0, len(dat), 0x10):
        ddat = dat[j:j + 0x10]
        f1, f2 = struct.unpack("II", ddat[0:8])
        extended = 4
        if f1 & extended:
            address = f1 >> 3
        else:
            address = f1 >> 21
        if addresses is not None:
            if address in addresses:
                dddat = ddat[8:8 + (f2 & 0xF)]
                if DEBUG:
                    print(f"  R 0x{address:x}: 0x{dddat.hex()}")
                ret.append((address, f2 >> 16, dddat, (f2 >> 4) & 0xFF))
        else:
            dddat = ddat[8:8 + (f2 & 0xF)]
            if DEBUG:
                print(f"  R 0x{address:x}: 0x{dddat.hex()}")
            ret.append((address, f2 >> 16, dddat, (f2 >> 4) & 0xFF))            
    return ret
parse_can_buffer = parse_can_bufferNEW
'''class PandaPlus(Panda):
    def __init__(self, serial=None):
        self._serial = serial
        self._handle = None
    
    def start(self, serial=None, claim=True):
        self._serial = serial
        self._handle = None
        self.connect(claim)    
        
    def can_recv(self, addresses = None): #modified to work with filter can buffer
        dat = bytearray()
        while True:
            try:
                dat = self._handle.bulkRead(1, 0x10 * 256)
                break
            except (usb1.USBErrorIO, usb1.USBErrorOverflow):
                print("CAN: BAD RECV, RETRYING")
                t.sleep(0.1)
        return parse_can_buffer(dat, addresses)'''



def formatBits(num, fmt, malt = 1): #!!!!!!! replace this with a proper module in CandaUtils
    
    start,size,mod = fmt.split(':')
    if fmt == '':
        return num	
    return format(int(((num>>int(start)) & ((1 << int(size)) - 1)) * malt), mod)



#class output(object):
#    def __init__(self, window: gui, name, canid = 0, fmt = '0:64:x', malt = 1):
#        self.window = window
#        self.name = name
#        self.mid = canid
#        self.fmt = fmt
#        self.maltiplyer = malt

#        self.window.openFrame('try')
        
#        row = self.window.gr()
        
#        self.window.addEntry('e' + self.name,row,0,0,1)
#        self.window.setEntryWidth('e' + self.name, 8)
#        self.window.setEntry('e' + self.name, fmt)
#        self.window.setEntrySubmitFunction('e' + self.name, self.updateFromat)
        
#        self.window.addEntry('em' + self.name, row, 1, 0, 1)
#        self.window.setEntryWidth('em' + self.name, 5)
#        self.window.setEntry('em' + self.name, malt)
#        self.window.setEntrySubmitFunction('em' + self.name, self.updateMalt)        
         
#        self.lab = self.window.addLabel('l' + self.name, "0000000000000000",row,2,0,1)
#        self.window.setLabelBg('l' + self.name, "white")
#        self.window.setLabelAlign('l' + self.name, "right")
#        self.window.setLabelWidth('l' + self.name, 16)
#        self.window.getLabelWidget('l' + self.name).config(font=("Courier New", 13))        
#        #Courier New
#        self.window.stopFrame()
#    def updateFromat(self):
#        self.fmt = self.window.getEntry('e' + self.name)      
    
#    def updateMalt(self):
#        self.maltiplyer = float(self.window.getEntry('em' + self.name))   
        
#    def set(self, value):
#        self.lab.config(text=formatBits(value, self.fmt, self.maltiplyer))
        
#class messageWindow():
#    def __init__(self, window: gui, name, address, ):
#        self.window = window
#        self.name = name
#        self.address = address

#        self.window.openScrollPane('left')
#        row = self.window.gr()

#        self.window.addEntry('e' + self.name, row,0,0,1)
#        self.window.setEntry('e' + self.name, name)

#        self.window.addEntry('e2' + self.name, row,1,0,1)
#        self.window.setEntry('e2' + self.name, address)

#        self.window.startFrame("try"+ self.name, row=row+1, column=0, colspan=2)
#        self.window.addLabel('lg'+ self.name, 'this is the first entry')
#        self.window.stopFrame()
#        self.window.stopScrollPane()


#message window output
currentMessage = None #global stores active message window
messagedict = {} #global stores list of message windows

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
        self.signals[name] = SignalOut(self.window, self.name+name, name)
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
        self.SignalValueLabel.config(text=str(value))


#Event functions for creating new messages and signals
def new():
    name = p.getEntry('name')
    currentMessage.addSignal(name)
#    focusMIDs.add(int(mid))
#    outputs.append(output(p, name, mid, fmt))
def mnew():
    mname = p.getEntry('mname')
    mmid = int(p.getEntry('mmid'), 16)
    messagedict[mmid] = messageWindow(p, mname, mmid)
#    outputs.append(messageWindow(p, mname, mmid))
                

#Manage Connecting to panda via Wifi or usb or run simulator
# Handles running the can input loop thread
def connectPanda():
    p.showSubWindow("con")
    t.sleep(2)
    try:
        #global dev
        dev.start()
        p.thread(runCan) 
    except:
        p.setLabel("ConnectStatus", "FAILED! Trying to connect to panda over Wifi")      
        print("FAILED! Trying to connect to panda over Wifi")      
                
        try:
            print('Trying panda')
            assert False  #!!!!!!!!!!!!!panda wifi donsn't timout
            #dev = Panda("WIFI")
        except:
            p.setLabel("ConnectStatus", "Connection timed out!\nClosing in 3 seconds")
            t.sleep(3)
            p.thread(simulater) 
            #app.stop()
            #sys.exit(0)    
    p.destroySubWindow('con')


#dictates what to do with the can message buffer
def processBuffer(buf):
    global messagedict
    for MID, _, xdata, bus in buf:
        if MID in messagedict:
            data = struct.unpack('>Q', xdata)[0]
            messagedict[MID].set(data)  
                    
#threds that loop and get the can message data
def simulater():
    ids = [0x120, 0x0e10]
    while 1:
        start = t.time()
        buffer = [(ids[randint(0, 1)], None, struct.pack('>Q',randint(0,0xffffffffffffffff)), 8) for o in range(8000//UPDATE_FREQUINCY)] #get data
        processBuffer(buffer) 
        dTime = t.time() - start
        print(dTime, end='\r')
        t.sleep(max((1/UPDATE_FREQUINCY)-(dTime), 0))        
def runCan():
    while 1:
        start = t.time()
        can_recv = dev.can_recv()#focusMIDs)
        processBuffer(can_recv)
        dTime = t.time() - start
        print(dTime, end='\r')
        t.sleep(max((1/UPDATE_FREQUINCY)-(dTime), 0))


#event to change the selected message window
def SelectMessageEvent():
    global currentMessage
    b = p.getRadioButton('messageSelect')
    currentMessage = messagedict[b]


        

p = gui("values")

p.setSticky("nesw")
p.setStretch("row")


#Can output----------------------------------------------

p.startScrollPane("MessagePane", row=0, column=0, disabled="horizontal")

p.setSticky("enw")
p.setBg("white")
p.setStretch("none")
p.addLabel('FM', "Message Name",0,0)
p.addLabel('ME', "MID",0,1)
p.addLabel('OT', "Value",0,2)

#p.setSticky("enw")
#p.setBg("white")
#p.setStretch("none")

#p.addLabel('FM', "Format",0,0)
#p.addLabel('ME', "Meter",0,1)
#p.addLabel('OT', "Value",0,2)

p.stopScrollPane()

currentMessage = messageWindow(p, 'test', 0x120)
messagedict[currentMessage.address] = currentMessage


#bit array output----------------------------------------------

p.startFrame("R", row=0, column=1)

p.setSticky("nesw")
p.setStretch("both")
for i in range(8):
    for x in range(8):
        p.addLabel(str(i)+str(x), randint(0,1), i,x,1,1)
        
p.stopFrame()


#signal creation----------------------------------------------

outputs = []
p.startFrame('bottom', row=1, colspan=2) 
focusMIDs = set()
p.addLabelEntry("name", 0,0)
p.addLabelEntry("mid", 0,1) 
p.addLabelEntry("fmt", 0,2)
p.setEntry("name", 'Test')
p.setEntry("mid", '120')
p.setEntry("fmt", "0:15:d")
p.addButton("Make Value", new, 0,3)

p.stopFrame()


#message creation------------------------------------------

p.startFrame('bottom2', row=2, colspan=2) 

p.addLabelEntry("mname", 0,0)
p.addLabelEntry("mmid", 0,1)
p.setEntry("mname", 'Test')
p.setEntry("mmid", '120')
p.addButton("mMake Value", new, 0,2)

p.stopFrame()


#Start-----------------------------------------------------

p.startSubWindow("con")
p.addLabel("ConnectStatus", "Connecting: USB") 
p.stopSubWindow()   

#p.thread(simulater)
#dev = PandaPlus()
p.setStartFunction(connectPanda)
p.go()


