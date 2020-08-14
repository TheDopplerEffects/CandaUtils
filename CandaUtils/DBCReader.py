
def extract(value:int, start:int, size:int):
    return value>>start&(1<<size)-1

class SignalClass():
    NO_RECIVER_NAME = 'XXX'
    DEFALT_UNIT = ''


    def __init__(self,
                 signal_name,
                 multiplexer_indicator,
                 start_bit, signal_size, 
                 byte_order, value_type, 
                 factor, offset, 
                 minimum, maximum,
                 unit = DEFALT_UNIT,
                 receiver = NO_RECIVER_NAME,):

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

    def decode(self, message): #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! implements envionment variable styled output
        return extract(message, self.start_bit, self.signal_size) * self.factor + self.offset

    def rawDecode(self, message):
        return extract(message, self.start_bit, self.signal_size) * self.fector + self.offset
class MessageClass():
    def __init__(self, massage_id:int, message_name:str, message_size:int, transmitter:str):
        self.massage_id = massage_id
        self.message_name = message_name
        self.message_size = message_size
        self.transmitter = transmitter
        self.__signals = []

    def addSignal(self, signal:SignalClass):
        self.__signals.append(signal)

    def __getitem__(self, MID:int):
        return self.signals[MID]

    def __iter__(self):
        return iter(self.__signals)

    def decode(self, message:int):
        return {sig.signal_name :sig.decode(message) for sig in self.__signals}
class DBCDecoder():

    #static methods for DBC file processing
    def __keyList(file:list):
        DBCObjects = []
        keys = {'VAL_','BU_','BO_','SG_',}

        for i in file:
            if not i.isspace() or i[0] != '\t':
                decon = i.strip().split(' ')
                if decon[0] in decon:
                    DBCObjects.append(decon)
        return DBCObjects
    def __removeVals(DBCObjects):
        vals = []
        for i, item in enumerate(DBCObjects):
            if item[0] == 'VAL_':
                vals.append(item)
                del(DBCObjects[i])
        return vals
    def __removeNodes(DBCObjects):     
        nodes = {}
        for i, item in enumerate(DBCObjects):
            if item[0] == 'BU_':
                nodes = nodes.union(item[1:])
                del(DBCObjects[i])
        return nodes

    def __init__(self, file):
        self._messages = dict()

        fileData = DBCDecoder.__keyList(file.readlines())
        vals = DBCDecoder.__removeVals(fileData)
        
        self._nodes = DBCDecoder.__removeNodes(file)

        for msg in fileData:
            if msg[0] == 'BO_':
                lineinfo = (int(msg[1]), msg[2][:-1], int(msg[3]), msg[4])
                lastMSG = MessageClass(*lineinfo)
                self._messages[lastMSG.massage_id] = lastMSG
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
    def __getitem__(self, MID):
        '''return the message object with the same message ID'''
        return self._messages[MID]
    def __iter__(self):
        '''return a list of all the messages in the DBC file'''
        return iter(self._messages.values())

    def getMessages(self):
        '''returns a list of all the message objects'''
        return self._messages.values()
    def addMessage(self, MID:int, message_name:str, message_size:int, transmitter:str):
        assert MID not in self._messages.keys(), 'Message already exists'
        message = MessageClass(*lineinfo)
        self._messages[message.massage_id] = message   
    def decode(self, MID:int, message:int) -> dict:
        '''
        returns finds the MID in the DBC file and returns its signal names as the key and the decode message as the value.
        Note: the value could be a int, float, string,

            MID: Message ID as an int
            message: the full message data as an int
        '''
        try:
            messageObj = self.__getitem__(MID)
            return messageObj.decode(message)
        except KeyError:
            return None

                
if __name__ == '__main__':
    print('Debug mode!')
    fileName = input("Please enter file name: ")
    if fileName == '':
        fileName = 'CandaUtils/test.dbc'

    with open(fileName, 'r') as f:
        DBC = DBCDecoder(f)


    for message in DBC:
        print(message.massage_id)
        for signal in message:
            print("\t"+signal.signal_name)
        print('\n')

    while 1:
        try:
            add = int(input('enter address:'), 16)
            msg = int(input('enter msg: '), 16)
            print(DBC[add].message_name)
            print('out = {}'.format(DBC.decode(add, msg)))

        except KeyboardInterrupt:
            break
    
