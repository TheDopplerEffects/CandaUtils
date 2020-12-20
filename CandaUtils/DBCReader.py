######  !!!!PROB TYPING BUGS test with numbers


class SignalClass():

    def __swapByteOrder(value:int, size:int):
        out = 0
        for i in range(size):
            out = (out<<8) + ((value>>i*8)&0xff)
        return out

    """
    extracts the bits from a value depending on the byte order.

    Note: big endian start is the most significant bit but it fallows a saw tooth pattern modeled by 

        (\left(8k-1\right)-\left(b-\operatorname{mod}\left(b,\ 8\right)+7-\operatorname{mod}\left(b,8\right)\right))

    the size extends to the least significant bit.
    little endian is converted to little endian then extrected as expected.

    """
    def __extract(value:int, start:int, size:int, valueLength:int, bigEndian:bool):
        if bigEndian:
            mostSignificant = 8 * valueLength - start - 8 + 2 * (x % 8) # 8k+-x-8+2\operatorname{mod}\left(x,\ 8\right)
            leastSignificant = mostSignificant - size + 1
            return value >> leastSignificant & (1 << size) - 1
            # return value>>start&(1<<size)-1
        else:
            return SignalClass.__swapByteOrder(value, valueLength)>>start+1-size&(1<<size)-1

    def __init__(self,
                 signal_name:str,
                 multiplexer_indicator,
                 start_bit:int, signal_size:int, 
                 byte_order:bool, value_type:bool, 
                 factor:float, offset:float, 
                 minimum:float, maximum:float,
                 unit:str = "",
                 receiver:str = 'Vector__XXX'):

        assert factor != 0, 'factor must not be 0'
        self.signal_name = signal_name
        self.multiplexer_indicator = multiplexer_indicator
        self.start_bit = start_bit
        self.signal_size = signal_size
        self.byte_order = byte_order #0=little endian, 1=big endian----------------implement order 
        self.value_type = value_type #+=unsigned, -=signed-------------------------implement sign
        self.factor = factor
        self.offset = offset
        self.minimum = minimum
        self.maximum = maximum
        self.unit = unit
        self.receiver = receiver
        self.descriptions = {}
    def __str__(self): #figure out how to add strings with + !!!
        return str('{} (start:{} size:{} factor:{} offset:{} receiver:{})'.format(self.signal_name, self.start_bit,self.signal_size, self.factor, self.offset, self.receiver, ))
    def decode(self, message, messageSize):
        try:
            return self.descriptions[int(SignalClass.__extract(message, self.start_bit, self.signal_size, messageSize, self.byte_order))] #How the hell are value descriptions handled with factors
        except KeyError:
            return SignalClass.__extract(message, self.start_bit, self.signal_size, messageSize, self.byte_order) * self.factor + self.offset
    def rawDecode(self, message):
        return SignalClass.__extract(message, self.start_bit, self.signal_size, messageSize, self.byte_order) * self.factor + self.offset
class MessageClass():
    def __init__(self, massage_id:int, message_name:str, message_size:int, transmitter:str):
        self.massage_id = massage_id
        self.message_name = message_name
        self.message_size = message_size
        self.transmitter = transmitter
        self.__signals = {}
    def __getitem__(self, name):
        return self.__signals[name]
    def __iter__(self):
        return iter(self.__signals.values())
    def __str__(self):
        return '{} (MID:{} Transmitter:{} Size:{})'.format(self.message_name, self.massage_id, self.transmitter, self.message_size)
    def addSignal(self, signal:SignalClass):
        self.__signals[signal.signal_name] = signal
    def decode(self, message:int):
        return {sigName :sig.decode(message, self.message_size) for sigName, sig in self.__signals.items()}
class DBCDecoder():
    #static methods for DBC file processing
    def __keyList(file:list):
        DBCObjects = []
        keys = {'BU_','BO_','SG_',}

        for i in file:
            if (not i.isspace()) and i[0] != '\t':
                if i.strip().startswith("VAL_"):
                    start, _, end = i.partition('"')
                    decode = [start]
                    while 1:
                        start, _, end = end.partition('"')
                        if end == '': break
                        decode += [start.strip()]
                    DBCObjects.append(decode[0].split() + decode[1:])
                    print(decode[0].split() + decode[1:])
                else:
                    decon = i.replace('  ', ' ').replace(';', '').replace('"', '').strip().split(' ') #removeing extra spaces after removeing " will remove empty units so DON'T
                    if decon[0] in keys:
                        DBCObjects.append(decon)
        return DBCObjects
    def __removeVals(DBCObjects):
        vals = [item for item in DBCObjects if item[0] == 'VAL_' and len(item) > 2]
        for i in vals:
            DBCObjects.remove(i)
        return vals
    def __removeNodes(DBCObjects):     
        nodes = {}
        for i, item in enumerate(DBCObjects):
            if item[0] == 'BU_':
                nodes = nodes.union(item[1:])
                del(DBCObjects[i - 1]) #this may will cause bug for sequential BU_ 
        return nodes
    def __deconstructBO(ls):
        return (int(ls[1]), ls[2][:-1], int(ls[3]), ls[4])
    def __deconstructSG(ls):
        datapos = ls[3][:-3].split('|')
        datamod = ls[4][1:-1].split(',')
        minmax = ls[5][1:-1].split('|')
        return (ls[1], ' ',
                int(datapos[0]), int(datapos[1]), 
                int(ls[3][-2]), 
                ls[3][-1], 
                float(datamod[0]), float(datamod[1]), 
                float(minmax[0]), float(minmax[1]), 
                ls[6][1:-1],
                ls[7])
    def __deconstructVAL(ls):
        return int(ls[1]), ls[2], {int(val):out for val,out in zip(ls[3::2], ls[4::2])}

    def __init__(self, file=''):
        if file != '':
            fileData = DBCDecoder.__keyList(file.readlines().copy())
            vals = DBCDecoder.__removeVals(fileData)
            self._nodes = DBCDecoder.__removeNodes(file)
            self._messages_byID = dict()
            self._messages_byName = dict()

            for msg in fileData:
                print(msg)
                if msg[0] == 'BO_':
                    lineinfo = DBCDecoder.__deconstructBO(msg)
                    lastMSG = MessageClass(*lineinfo)
                    self._messages_byID[lastMSG.massage_id] = lastMSG
                    self._messages_byName[lastMSG.message_name] = lastMSG
                elif msg[0] == 'SG_':
                    sig = SignalClass(*DBCDecoder.__deconstructSG(msg))
                    lastMSG.addSignal(sig)

            for val in vals:
                print(val)
                id, name, convert = DBCDecoder.__deconstructVAL(val)
                self._messages_byID[id][name].descriptions = convert
        else:
            self._messages_byID = dict()
            self._messages_byName = dict()
            self._nodes = []
    def __getitem__(self, key):
        '''return the message object with the same message ID'''
        if isinstance(key, str):
            assert key in self._messages_byName.keys(), 'Message name  ' + key + ' does not exist'
            return self._messages_byName[key]
        else:
            assert key in self._messages_byID.keys(), 'Message ID ' + str(key) + ' does not exist'
            return self._messages_byID[key]
    def __iter__(self):
        '''return a list of all the messages in the DBC file'''
        return iter(self._messages_byName.values())

    def getMessages(self):
        '''returns a list of all the message objects'''
        return self._messages_byName.values()
    def add(self, message:MessageClass):
        assert message.massage_id not in self._messages_byID.keys(), 'Message ID already exists'
        assert message.message_name not in self._messages_byName.keys(), "Message name already exists"
        self._messages_byID[message.massage_id] = message   
        self._messages_byName[message.message_name] = message
    def remove(self, key):
        item = self.__getitem__(key)
        self._messages_byID.pop(item.massage_id)
        self._messages_byName.pop(item.message_name)
        

    def decode(self, MID:int, message:int) -> dict:
        '''
        returns finds the MID in the DBC file and returns its signal names as the key and the decode message as the value.
        Note: the value could be a int, float, string,

            MID: Message ID as an int
            message: the full message data as an int
        '''
        return self._messages_byID[MID].decode(message)


if __name__ == '__main__':

    print('Debug mode!')
    f = None
    while not f:
        try:
            fileName = input("Please enter file name: ")
            if fileName == '':
                fileName = 'CandaUtils/test.dbc'
            with open(fileName, 'r') as f:
                DBC = DBCDecoder(f)
        except IOError:
            f = None
            print(f'no file named {fileName}')

    for message in DBC:
        print(message)
        for signal in message:
            print("\t",signal)
            if signal.descriptions:
                print("\t\t",signal.descriptions)
        print('\n')

    while 1:
        DBC.remove("GEARBOX")
        add = int(input('enter address:'))
        msg = int(input('enter msg: '), 16)
        print(DBC[add])
        print('out = {}'.format(DBC.decode(add, msg)))    
