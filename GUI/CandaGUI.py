from appJar import gui
from random import randint
import time as t
from panda import Panda
import struct 

DEBUG = 0

UPDATE_FREQUINCY = 10 #hz

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

class PandaPlus(Panda):
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
        return parse_can_buffer(dat, addresses)
    




def formatBits(num, fmt, malt = 1): #!!!!!!! replace this with a proper module in CandaUtils
    
    start,size,mod = fmt.split(':')
    if fmt == '':
        return num	
    return format(int(((num>>int(start)) & ((1 << int(size)) - 1)) * malt), mod)

class output(object):
    def __init__(self, window: gui, name, canid = 0, fmt = '0:64:x', malt = 1):
        self.window = window
        self.name = name
        self.mid = canid
        self.fmt = fmt
        self.maltiplyer = malt

        self.window.openScrollPane('left')
        
        row = self.window.gr()
        
        self.window.addEntry('e' + self.name,row,0,0,1)
        self.window.setEntryWidth('e' + self.name, 8)
        self.window.setEntry('e' + self.name, fmt)
        self.window.setEntrySubmitFunction('e' + self.name, self.updateFromat)
        
        self.window.addEntry('em' + self.name, row, 1, 0, 1)
        self.window.setEntryWidth('em' + self.name, 5)
        self.window.setEntry('em' + self.name, malt)
        self.window.setEntrySubmitFunction('em' + self.name, self.updateMalt)        
        
        self.lab = self.window.addLabel('l' + self.name, "0000000000000000",row,2,0,1)
        self.window.setLabelBg('l' + self.name, "white")
        self.window.setLabelAlign('l' + self.name, "right")
        self.window.setLabelWidth('l' + self.name, 16)
        self.window.getLabelWidget('l' + self.name).config(font=("Courier New", 13))        
        #Courier New
        self.window.stopScrollPane()
    def updateFromat(self):
        self.fmt = self.window.getEntry('e' + self.name)      
    
    def updateMalt(self):
        self.maltiplyer = float(self.window.getEntry('em' + self.name))   
        
    def set(self, value):
        self.lab.config(text=formatBits(value, self.fmt, self.maltiplyer))
        
def new():
    name = p.getEntry('name')
    mid = int(p.getEntry('mid'), 16)
    fmt = p.getEntry('fmt')
    focusMIDs.add(int(mid))
    outputs.append(output(p,name, mid, fmt))   
                
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
                   
    
    
            
            
        
def simulater():
    ids = [0x120, 0x0e10]
    while 1:
        start = t.time()
        buffer = [(ids[randint(0, 1)], None, struct.pack('>Q',randint(0,0xffffffffffffffff)), 8) for o in range(8000//UPDATE_FREQUINCY)] #get data
        for MID, _, xdata, bus in buffer:
            data = struct.unpack('>Q', xdata)[0]
            for d in outputs: #Data Distrobution betwean the output lines
                if d.mid == MID:
                    d.set(data)    
        dTime = t.time() - start
        print(dTime, end='\r')
        t.sleep(max((1/UPDATE_FREQUINCY)-(dTime), 0))
        
def runCan():
    while 1:

        start = t.time()
        can_recv = dev.can_recv()#focusMIDs)
        for MID, _, xdata, bus in can_recv:
            data = struct.unpack('>Q', xdata)[0]
            for d in outputs: #Data Distrobution betwean the output lines
                if d.mid == MID:
                    d.set(data)      
        dTime = t.time() - start
        print(dTime, end='\r')
        t.sleep(max((1/UPDATE_FREQUINCY)-(dTime), 0))

        

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

focusMIDs = set()

p.addLabelEntry("name", 0,0)
p.addLabelEntry("mid", 0,1)
p.addLabelEntry("fmt", 0,2)
p.setEntry("name", 'Test')
p.setEntry("mid", '10')
p.setEntry("fmt", "0:15:d")
new()
p.setEntry("name", 'Tes')
p.setEntry("mid", '10')
p.setEntry("fmt", "16:15:d")
new()
p.setEntry("name", 'Ttgst')
p.setEntry("mid", '10')
p.setEntry("fmt", "32:15:d")
new()
p.addButton("Make Value", new, 0,3)

p.stopFrame()

p.startSubWindow("con")
p.addLabel("ConnectStatus", "Connecting: USB") 
p.stopSubWindow()   

#p.thread(simulater)
dev = PandaPlus()
p.setStartFunction(connectPanda)
p.go()


