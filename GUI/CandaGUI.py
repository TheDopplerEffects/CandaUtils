from appJar import gui
from random import randint
import time
from panda import Panda
import sys
import os
import struct

DEBUG = False
DEBUG_WITH_SIM = True
UPDATE_FREQUINCY = 10  # hz

# inject custom methods to panda


def parse_can_bufferNEW(dat, addresses=None):
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

    def can_recv(self, addresses=None):  # modified to work with filter can buffer
        dat = bytearray()
        while True:
            try:
                dat = self._handle.bulkRead(1, 0x10 * 256)
                break
            except (usb1.USBErrorIO, usb1.USBErrorOverflow):
                print("CAN: BAD RECV, RETRYING")
                time.sleep(0.1)
        return parse_can_buffer(dat, addresses)


def formatBits(num, fmt, malt=1):  # !!!!!!! replace this with a proper module in CandaUtils

    start, size, mod = fmt.split(':')
    if fmt == '':
        return num
    return format(int(((num >> int(start)) & ((1 << int(size)) - 1)) * malt), mod)


# message window output
currentMessage = None  # global stores active message window
messageByMID = {}  # global stores list of message windows
messageByName = {}


class messageWindow():
    def __init__(self, window: gui, name: str, address: int, ):
        self.window = window
        self.name = name
        self.address = address
        self.signals = {}

        self.window.openScrollPane('MessagePane')
        nextRow = self.window.gr()

        # Message select
        self.window.addRadioButton("messageSelect", name)
        self.window.setRadioButtonChangeFunction('messageSelect', SelectMessageEvent)

        # Message MID label
        self.window.addLabel('Address' + self.name, address, nextRow, 1, 0, 1)
        self.window.setLabelWidth('Address' + self.name, 5)

        # Message value
        self.messageValueLabel = self.window.addLabel('Value' + self.name, "FFFFFFFFFFFFFFFF", nextRow, 2,)
        self.window.getLabelWidget('Value' + self.name).config(font=("Courier New", 13))

        # Signals frame
        self.window.setPadding((20, 0))
        self.window.startFrame("SigFrame" + self.name, row=nextRow + 1, column=0, colspan=4)
        self.window.setBg('yellow')
        self.window.stopFrame()
        self.window.setPadding((0, 0))

        self.window.stopScrollPane()

    def set(self, value):
        self.messageValueLabel.config(text=f'{value:016x}')
        for i in self.signals.values():
            i.set(value)

    def addSignal(self, name):
        self.window.openFrame("SigFrame" + self.name)
        self.signals[name] = SignalOut(self.window, self.name + name, name)
        self.window.stopFrame()


class SignalOut():
    def __init__(self, window, id, name):
        self.name = name
        self.id = id
        self.window = window

        nextRow = self.window.gr()

        self.window.addLabel('signalName' + self.id, name, nextRow, 0, 0, 1)

        self.SignalValueLabel = self.window.addLabel('signalValue' + self.id, "FFFFFFFFFFFFFFFF", nextRow, 2, 0, 1)
        self.window.setLabelAlign('signalValue' + self.id, "right")
        self.window.setLabelWidth('signalValue' + self.id, 16)
        self.window.getLabelWidget('signalValue' + self.id).config(font=("Courier New", 13))

    def set(self, value):
        self.SignalValueLabel.config(text=f'{value:016x}')


# Event functions for creating new messages and signals
def new():
    name = p.getEntry('name')
    if name in currentMessage.signals:
        p.bell()
    else:
        currentMessage.addSignal(name)


def mnew():
    mname = p.getEntry('mname')
    mmid = int(p.getEntry('mmid'), 16)
    if mmid in messageByMID or mname in messageByName:
        p.bell()
    else:

        temp = messageWindow(p, mname, mmid)
        messageByName[mname] = temp
        messageByMID[mmid] = temp
        currentMessage = temp


# Manage Connecting to panda via Wifi or usb or run simulator
# Handles running the can input loop thread
def connectPanda():
    if not DEBUG_WITH_SIM:
        try:
            global dev
            dev.start()
            p.thread(runCan)
            p.destroySubWindow('Connect')
        except AssertionError:  # Panda usb connection error is presented as a assert and isn't descriptive
            p.setLabel("ConnectStatus", "FAILED!\nTrying to connect to panda over Wifi")
            if DEBUG:
                print("FAILED! Trying to connect to panda over Wifi")
            try:
                if DEBUG:
                    print('Trying panda')
                raise  # !!!!!!!!!!!!!panda wifi donsn't timout
                dev.start("WIFI")
                p.destroySubWindow('Connect')
                p.thread(runCan)
            except:
                p.setLabel("ConnectStatus", "Unable to find Panda!\nClosing in 3 seconds")
                time.sleep(3)
                p.stop()
    else:
        p.destroySubWindow('Connect')
        p.setTitle('Canda ( SIMULATOR MODE )')
        p.thread(simulater)
        p.show()


# Used as a way to update the data output in the main loop
def updateWithMessage(msgData):
    global messageByMID
    for MID, xdata, bus in msgData:
        if MID in messageByMID:
            data = struct.unpack('>Q', xdata)[0]
            messageByMID[MID].set(data)


# dictates what to do with the can message buffer
def processBuffer(buf):
    usedMIDs = set()
    outputData = []
    for MID, _, xdata, bus in reversed(buf):
        if MID not in usedMIDs:
            usedMIDs.add(MID)
            outputData.append([MID, xdata, bus])
    p.queueFunction(updateWithMessage, outputData)


# threds that loop and get the can message data
def simulater():
    ids = [0x120, 0x0e10]
    while 1:
        start = time.time()
        buffer = [(ids[randint(0, 1)], None, struct.pack('>Q', randint(0, 0xffffffffffffffff)), 8) for o in range(8000 // UPDATE_FREQUINCY)]  # get data
        processBuffer(buffer)
        dTime = time.time() - start
        print(dTime, end='\r')
        time.sleep(max((1 / UPDATE_FREQUINCY) - (dTime), 0))


def runCan():
    while 1:
        start = time.time()
        can_recv = dev.can_recv()  # focusMIDs)
        processBuffer(can_recv)
        dTime = time.time() - start
        print(dTime, end='\r')
        time.sleep(max((1 / UPDATE_FREQUINCY) - (dTime), 0))


# event to change the selected message window
def SelectMessageEvent():
    global currentMessage
    global messageByName
    b = p.getRadioButton('messageSelect')
    currentMessage = messageByName[b]


tools = ['mail', 'zoom-in']
tbFunc = [mnew, new]

p = gui("Canda")


p.setSticky("nesw")
p.setStretch("row")

# Can output----------------------------------------------

p.startScrollPane("MessagePane", row=0, column=0, disabled="horizontal")

p.setSticky("enw")
p.setBg("white")
p.setStretch("none")
p.addLabel('FM', "Message Name", 0, 0)
p.addLabel('ME', "MID", 0, 1)
p.addLabel('OT', "Value", 0, 2)
p.setLabelWidth('OT', 16)

p.stopScrollPane()


# bit array output----------------------------------------------

p.startFrame("R", row=0, column=1)

p.setSticky("nesw")
p.setStretch("both")
for i in range(8):
    for x in range(8):
        p.addLabel(str(i) + str(x), randint(0, 1), i, x, 1, 1)

p.stopFrame()


# signal creation----------------------------------------------

outputs = []
p.startFrame('bottom', row=1, colspan=2)
focusMIDs = set()
p.addLabelEntry("name", 0, 0)
p.addLabelEntry("mid", 0, 1)
p.addLabelEntry("fmt", 0, 2)
p.setEntry("name", 'Test')
p.setEntry("mid", '120')
p.setEntry("fmt", "0:15:d")
p.addButton("Make Value", new, 0, 3)

p.stopFrame()


# message creation------------------------------------------

p.startFrame('bottom2', row=2, colspan=2)

p.addLabelEntry("mname", 0, 0)
p.addLabelEntry("mmid", 0, 1)
p.setEntry("mname", 'Test')
p.setEntry("mmid", '120')
p.addButton("mMake Value", mnew, 0, 2)

p.stopFrame()


# Start-----------------------------------------------------

dev = PandaPlus()

p.startSubWindow("Connect")
p.setPadding((10, 10))
p.setStretch("none")
p.addLabel("ConnectStatus", "Connecting to USB\n ", 0, 0, 0, 0)
p.stopSubWindow() p.addToolbar(tools, tbFunc, findIcon=True) 
p.setStartFunction(connectPanda) 
p.go(startWindow='Connect') 
