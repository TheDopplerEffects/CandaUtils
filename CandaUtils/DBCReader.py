class signal():
    def __init__(self):
        self.name = name
        self.startBit = start
        self.size = size
        self.sign = sign
        self.scale = scale
        self.offset = offset
        self.minval = minval
        self.maxval = maxval
        
    def string(line):
        elements = line.split(' ')  # SG_ STEER_SENSOR_STATUS_1 : 34|1@0+ (1,0) [0|1] "" EON
        
        self.name = elements[1]
        
        decodeInfo = elements[3].split('@')[0].split('|')
        self.startBit = int(decode[0])
        self.size = int(decode[1])
        
        decodeMod = elements[4][1:-1].split(',')
        self.scale = decodeMod[0]
        self.offset = decodeMod[1]
        
        decodeMinMax = elements[5][1:-1].split('|')
        self.minval = decodeMinMax[0]
        self.maxval = decodeMinMax[1]
        
    def decode(num):
        pass
        


def loadDBC(fileName):
    with open(fileName, 'r'):
        pass
    
