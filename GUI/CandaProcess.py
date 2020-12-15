import multiprocessing as mp
from random import randint

def updateLoop(val, lockObj):
    while True:
        for i in range(0xffff):
            address = randint(0, 0xFFFF)
            data = (randint(0, 0xFFFF) << 48) + (i << 32)+ randint(0, 0xFFFFFFFF)
            
            lockObj.acquire()
            val[0] = address
            val[1] = data
            lockObj.release()

if __name__ == "__main__":
    i = [0,0]
    l = mp.Lock()

    p = mp.Process(target=updateLoop, args=[i, l])
    p.start()
    
    for i in range(10000):
        l.acquire()
        print(i)
        l.release()
    p.kill()

