class Observer():
	def update(self, subject: ValueUpdateSubject):
		pass

class ValueUpdateSubject():
	def __init__(self, messageObj, lockObj):
		self.__observers = set()
		self.__messageData = array
		self.__lock = lock
		self._data = dict() #Key is Message id and value is the message object
	def add(self, observer: Observer):
		self.__obeservers.add(observer)

	def remove(self, observer: Observer):
		self.__observers.remove(observer)

	def __getData(self):
		self.__lock.acquire()
		for i in self.__messageData:
			self._data[i] = self.__messageData[i]

	def update(self):
		self.__getData()	
		for i in self.__observers:
			i.update(self)

