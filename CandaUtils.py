from appJar import gui
from math import *

'''
class node(object):
    def __init__(self,d = None, n = None):
        self.__data = d
        self.__next = n
        self.__parent = None
    def __add__(self, other):
'''

def realOnesComplement(bits, size):
    return bits ^ int('1'*size-1,2)

def realTwosComplement(bits, size):
    return bits ^ int('1'*size-1,2)-1


class DataInfo(object):
    def __init__(self, window = None):
        self.__window = window

        self._rawData = 0
        self.__start = 0
        self.__length = 64
        self.__point = 0
        self.__style = ''
        self.__operations = ''
        self.__pad = '0'

        self._id = 0
        self.dataName = 'Unknown'
        self.group = 'None'


    def __str__(self):
        return ('{:'+ self.__pad + str(self.__length) + self.__style +'}').format(self._rawData)
    def __len__(self):
        return self.__length
    def __lt__(self, anotherObj):
        return self._rawData < anotherObj
    def __int__(self):
        return int(self._rawData)
    def __le__(self, anotherObj):
        return self._rawData <= anotherObj
    def __eq__(self, anotherObj):
        return self._rawData == anotherObj
    def __ne__(self, anotherObj):
        return self._rawData != anotherObj
    def __gt__(self, anotherObj):
        return self._rawData > anotherObj
    def __ge__(self, anotherObj):
        return self._rawData >= anotherObj
    def __add__(self, anotherObj):
        return self._rawData + anotherObj
    def __sub__(self, anotherObj):
        return self._rawData - anotherObj
    def __mul__(self, anotherObj):
        return self._rawData * anotherObj
    def __truediv__(self, anotherObj):
        return self._rawData / anotherObj 
    def __floordiv__(self, anotherObj):
        return self._rawData // anotherObj
    def __rmul__(self, anotherObj):
        return anotherObj * self._rawData
    def __rtruediv__(self, anotherObj):
        return anotherObj / self._rawData 
    def __rfloordiv__(self, anotherObj):
        return anotherObj // self._rawData

    def len(self):
        return self.__length
  

    def setFormat(self, start, bitLength, output = '', ops = '', point = 0):
        self.__length = bitLength
        self._rawData &= int('1'*bitLength,2) 
        self.__start = start
        self.__style = output
        self.__operations = ops
        self.__point = point

    def set(self, val):
        self._rawData = val>>self.__start & int('1'*self.__length,2)

        for i in self.__operations:
            if i == '1':
                self._rawData = self._rawData ^ int('1'*self.__length-1,2)
            elif i == '2':
                self._rawData = self._rawData ^ int('1'*self.__length-1,2) + 1
            elif i == 'r':
                rev = 0

                while self._rawData > 0:
                    rev <<= 1
                    if self._rawData & 1 == 1:
                        rev ^= 1
                    self._rawData >>= 1 
                self._rawData = ~self._rawData
            




        



        




if __name__ == '__main__':
    app = gui()
    progress = 0
    def addbar():
        pass
    
    def update():
        global progress 
        progress = app.getEntry('1')
        if progress is None:
            progress = 0
        app.setMeter('progress', progress)
    
    #class valbox(object):
    #    def __init__(self, Stream = None, )
    
    def press(name):
        if name == 'Exit':
            app.stop()
        else: 
            try:
                firstnum = int(app.getEntry('first'))
                secondNum = int(app.getEntry('sn'))
    
                message = 'The results are as fallows \n\n'
                message += 'add' + str(firstnum + secondNum) + '\n'
    
                if name == 'Result':
                    app.setLabel('result', message)
                elif name == 'MessageBox Redult':
                    app.infoBox('Result', message)
    
            except ValueError as e:
                app.errorBox('Error', 'Invalid Number')
                app.setFocus('first') 
    
    app.addNumericEntry('1')
    app.addMeter('progress')
    app.setMeterFill('progress', 'blue')
    app.setMeter('progress', progress)
    
    app.registerEvent(update)
    
    
    
    app.go()