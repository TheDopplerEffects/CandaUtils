import multiprocessing as mp
from random import randint


class ComProcess(mp.Process):
    def __init__(self):
        super(ComProcess, self).__init__()
        manager = mp.Manager()
        self.__data = manager.dict()
        self.__lock = manager.Lock()
    
    def run(self):
        MIDs = {0x1111, 0x6969, 0xff00}
        cnt = 0
        while True:
            for ID in MIDs:
                data = (randint(0, ID) << 48) + (cnt << 32)+ randint(0, 0xFFFFFFFF)
                cnt += 1
                if cnt > 0xffff: cnt = 0
                self.__lock.acquire()
                self.__data[ID] = data
                self.__lock.release()

    def getData(self):
        return self.__data

    def getLock(self):
        return self.__lock

if __name__ == "__main__":
    process = ComProcess()
    process.start()

    data = process.getData()
    lock = process.getLock()
    for i in range(10000):
        lock.acquire()
        print(data)
        lock.release()
    process.kill()

