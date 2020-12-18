class Observer():
	def update(self, subject):
		pass

class ValueUpdateSubject():
	def __init__(self, messageObj, lockObj):
		self.__observers = set()
		self.__messageData = messageObj
		self.__lock = lockObj
		self._data = dict() #Key is Message id and value is the message object
	def add(self, observer: Observer):
		self.__observers.add(observer)

	def remove(self, observer: Observer):
		self.__observers.remove(observer)

	def __getData(self):
		self.__lock.acquire()
		for i in self.__messageData:
			self._data[i] = self.__messageData[i]
		self.__lock.release()

	def update(self):
		self.__getData()	
		for i in self.__observers:
			i.update(self) # this can probibly be faster

