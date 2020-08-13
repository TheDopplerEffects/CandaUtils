


def keyList(file:list):
    DBCObjects = []
    keys = {'VAL_','BU_','BO_','SG_',}

    for i in file:
        if not i.isspace() or i[0] != '\t':
            decon = i.strip().split(' ')
            if decon[0] in decon:
                DBCObjects.append(decon)
    return DBCObjects

def removeVals(DBCObjects):
    vals = []
    for i, item in enumerate(DBCObjects):
        if item[0] == 'VAL_':
            vals.append(item)
            del(DBCObjects[i])
    return vals

def removeNodes(DBCObjects):     
    nodes = {}
    for i, item in enumerate(DBCObjects):
        if item[0] == 'BU_':
            nodes = nodes.union(item[1:])
            del(DBCObjects[i])
    return nodes

class SignalClass():
    def __init__(self,
                 signal_name,
                 multiplexer_indicator,
                 start_bit, signal_size, 
                 byte_order, value_type, 
                 factor, offset, 
                 minimum, maximum,
                 unit = '',
                 receiver = 'XXX',
                 ):

        assert factor != 0, 'factor must not be 0'
        self.signal_name = signal_name
        self.multiplexer_indicator = multiplexer_indicator
        self.start_bit = start_bit
        self.signal_size = signal_size
        self.byte_order = byte_order #0=little endian, 1=big endian
        self.value_type = value_type #+=unsigned, -=signed
        self.factor = factor
        self.offset = offset
        self.minimum = minimum
        self.maximum = maximum
        self.unit = unit
        self.receiver = receiver
        self.Environment_Variable = None

    def decode(self):
        pass

class MessageClass():
    def __init__(self, massage_id:int, message_name:str, message_size:int, transmitter:str):
        self.massage_id = massage_id
        self.message_name = message_name
        self.message_size = message_size
        self.transmitter = transmitter
        self.signals = []

    def addSignal(self, signal:SignalClass):
        self.signals.append(signal)

class DBCDecoder():
    def __init__(self, file):
        self.messages = dict()

        fileData = keyList(file.readlines())
        vals = removeVals(fileData)
        
        self.nodes = removeNodes(file)

        for msg in fileData:
            if msg[0] == 'BO_':
                lineinfo = (int(msg[1]), msg[2][:-1], int(msg[3]), msg[4])
                lastMSG = MessageClass(*lineinfo)
                self.messages[lastMSG.massage_id] = lastMSG
            elif msg[0] == 'SG_':
                datapos = msg[3][:-3].split('|')
                datamod = msg[4][1:-1].split(',')
                minmax = msg[5][1:-1].split('|')
                sig = SignalClass(msg[1], ' ',
                                       int(datapos[0]), int(datapos[1]), 
                                       int(msg[3][-2]), 
                                       msg[3][-1], 
                                       float(datamod[0]), float(datamod[1]), 
                                       float(minmax[0]), float(minmax[1]), 
                                       msg[6][1:-1],
                                       msg[7]
                                       )
                lastMSG.addSignal(sig)
                
                
if __name__ == '__main__':
    print('Debug mode!')
    fileName = input("Please enter file name: ")
    if fileName == '':
        fileName = 'CandaUtils/test.dbc'
    with open(fileName, 'r') as f:
        DBC = DBCDecoder(f)

    for keys, i in DBC.messages.items():
        print(i.massage_id)
        for k in i.signals:
            print("\t"+k.signal_name)
        print('\n')
    
