import multiprocessing as mp
from random import randint



def updateLoop(messageObj, lockObj):
    MIDs = {0x1111, 0x6969, 0xff00}
    cnt = 0
    while True:
        for ID in MIDs:
            data = (randint(0, 0xFFFF) << 48) + (cnt << 32)+ randint(0, 0xFFFFFFFF)
            cnt += 1
            if cnt > 0xffff: cnt = 0
            lockObj.acquire()
            messageObj[ID] = data
            lockObj.release()

if __name__ == "__main__":
    manager = mp.Manager()
    data = manager.dict()
    lock = manager.Lock()
    process = mp.Process(target=updateLoop, args=[data, lock])
    process.start()

    for i in range(10000):
        lock.acquire()
        print(data)
        lock.release()
    process.kill()

