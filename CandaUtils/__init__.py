from appJar import gui
from math import *


class DataInfo(object):
    def __init__(self, start = 0, bitLength = 64, style = '', pad = "0"):
        '''
        For managing the use of bin/hex/int numbers in raw form

        Parameters:
            start     : starting bit
            bitLength : number of bits in the data
            style     : text output style ie b = binary, x = hex, i = intiger
            pad       : the padding char for text output '' = space padding, '0' = zero padding
        '''
        self._rawData = 0
        self._value = 0
        self.__start = start
        self.__length = bitLength
        self.__Maltiplyer = 1
        self.setTextFormat(start, bitLength, style, pad)

        self._id = 0
        self.dataName = 'Unknown'
        self.group = 'None'

    #Typical Dunders
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

    def __str__(self):
        return ('{:'+ self.__pad + str(self.__length) + self.__style +'}').format(self._rawData)
    def len(self):
        return self.__length
  

    def setFormat(self, start, bitLength, style = '', pad = "0"):
        self.__length = bitLength
        self._rawData &= int('1'*bitLength,2) 
        self.__start = start
        self.__style = style
        self.__pad = pad

        self.__TextFormat = f'{str(start)}:{str(bitLength)}:{pad}{output}'

    def setTextFormat(self, fmt):
        self.__start, self.__length, *mod = fmt.split(":")
        self.__pad = "0"
        self.__style = ""

        if mod.len():
            if mod[0] == '0':
                self.__pad = "0"
            for i in mod:
                if i == 'b':
                    self.__style = 'b'
                if i == 'x':
                    self.__style = 'x'
                if i == 'i':
                    self.__style = ''
                
        self._rawData &= int('1'*bitLength,2) 

    def setMaltiplyer(self, malt):
        self.__Maltiplyer = malt

    def setId(self, frameID):
        self._id = frameID

    def setNumber(self, val):
        self._rawData = val>>self.__start & int('1'*self.__length,2)
        self._value = (self._rawData * self.__Maltiplyer)

    def getNumber(self):
        return self._rawData

    def getFormatted(self):
        return self.__str__()

            




        



        




