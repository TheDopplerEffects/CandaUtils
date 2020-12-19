from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import randint
import Observer



colors = ['red', 'green', 'blue', 'pink', 'orange', 'black']

class Color(QWidget):
	def __init__(self, color, *args, **kwargs):
		super(Color, self).__init__(*args, **kwargs)

		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)
class BitLabel(QLabel):
	def __init__(self, value=False):
		super(BitLabel, self).__init__()
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QPalette.Window, QColor("gray"))
		self.setPalette(palette)
		self.setAlignment(Qt.AlignCenter)

		if (value):
			val = 1
		else:
			val = 0
		self.setText(str(val))
		self.setMinimumWidth(13)

	def setBit(self, value):
		if (value):
			val = 1
		else:
			val = 0
		self.setText(str(val))
class SquareBitArray(QWidget):
	def __init__(self, columns, rows):
		super(SquareBitArray, self).__init__()

		binArray = QGridLayout()
		self.setLayout(binArray)
		self.bits = [[] for i in range(rows)]

		for i in range(columns):
			for o in range(rows):
				newLabel = BitLabel()
				binArray.addWidget(newLabel, o, i)
				self.bits[o].append(newLabel)
class SignalWidget(QWidget):
	def __init__(self, name="Message Label", number=0):
		super(SignalWidget, self).__init__()

		self.nameLabel = QLabel(str(name))
		self.name = name
		self.nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.numberLabel = QLabel((f'{number:016x}'))
		self.numberLabel.alignment = Qt.AlignRight
		self.numberLabel.setFont(QFont("Courier New", weight=QFont.Bold))

		hLayout = QHBoxLayout(self)
		hLayout.addSpacing(10)
		hLayout.addWidget(self.nameLabel)
		hLayout.addWidget(self.numberLabel)
		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

	"""
	displays a value after after decoding

	value int: full binary message to be decoded and displayed
	"""
	def setValue(self, value):
		self.numberLabel.setText(f'{value:016x}')

	"""
	sets the name of the signal

	name str: name of the signal
	"""
	def setName(self, name):
		self.nameLabel.setText(name)
class MessageWidget(QWidget):
	def __init__(self, name='New Message', MID=0): #-----------------MID not implemented
		super(MessageWidget, self).__init__()
		self.signals = {}
		self.name = name
		self.MID = MID
		#self.name.setFont(QFont("Times", weight=QFont.Bold))
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(QLabel(name))
		self.setLayout(self.mainLayout)

	"""
	Adds Signal widget

	name signalWidget: the signal widget being added
	"""
	def addSignal(self, signalWidget):
		self.mainLayout.addWidget(signalWidget)
		self.signals[signalWidget.name] = signalWidget

	"""
	remove Signal by name

	name str: name the the signal
	"""
	def removeSignal(self, name):
		pass

	"""
	disctribute a value to all the message objects created in this self witch the display that data

	value int: binary data sent to all signals to be displayed
	"""
	def distributeSignals(self, value):
		for i in self.signals:
			self.signals[i].setValue(value) # I think i can do this faster

	def mousePressEvent(self, event):
		self.parent.messageSelected = self
		print(self.MID)
class MessageListWidget(QScrollArea):
	def __init__(self, *args, **kwargs):
		super(MessageListWidget, self).__init__(*args, **kwargs)

		self.messageLayoutBox = QVBoxLayout()
		self.messageLayoutBox.setAlignment(Qt.AlignTop)
		self.messages = dict()
		self.setMinimumWidth(200)

		containerWidget = QWidget() 
		containerWidget.setLayout(self.messageLayoutBox)

		# sw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.setWidgetResizable(True)
		self.setWidget(containerWidget)

	"""
	creats a new MessageWidget Object

	massage MessageWidget: the message widget being added
	"""
	def addMessage(self, message):
		assert (message.name not in self.messages.keys()), f'{name}" already exists'
		assert message.name.strip() != '', "massage name can't be nothing"
		self.messages[message.name] = message
		self.messageLayoutBox.addWidget(message)

	"""
	removes a MessageWidget object from the made message widgets

	name str: the name of the MessageWidget
	"""
	def removeMessage(self, name):
		assert name in self.messages.keys, f'{name}" does not exists'
		assert name.strip() != '', "massage name can't be nothing already exists"
		pass

	"""
	returns a Messagewidget Object by name.

	name str: the name of the MessageWidget
	"""
	def getMessage(self, name):
		assert name in self.messages.keys, f'{name}" does not exists'
		assert name.slice() != '', "massage name can't be nothing already exists"
		return self.messages[name]

	



class MainWindow(QMainWindow):
	class __MessageObserver(Observer.Observer):
		def __init__(self, labelFunc, MID):
			self.MID = MID
			self.labelFunc = labelFunc
		def update(self, subject: Observer.ValueUpdateSubject):
			if self.MID in subject._data:
				self.labelFunc(subject._data[self.MID])
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.messageSelected = None
		self.__subject = None
		self.updateRate = 10
		self.setWindowTitle("Canda")
		self.setMinimumSize(800,600 )

		self.bitMatrix = SquareBitArray(8, 8)
		rightZone = QVBoxLayout()
		rightZone.addWidget(self.bitMatrix)
		rightZone.addWidget(Color('green'))
		rightZoneWidget = QWidget()
		rightZoneWidget.setLayout(rightZone)

		centerZone = Color('blue')

		self.messageListWidget = MessageListWidget(parent=self)

		mainWidget = QSplitter(Qt.Horizontal)
		mainWidget.addWidget(self.messageListWidget)
		mainWidget.addWidget(centerZone)
		mainWidget.addWidget(rightZoneWidget)

		self.setCentralWidget(mainWidget)

	"""
	stores a Subject object to add new observers to. note: new observers best be made after a Subject is set

	subject Object: any subject or subject like object
	"""
	def setSubject(self, subject):
		self.__subject = subject

	"""
	adds a MessageWidget

	name str: name of the message widget
	MID int: the message id of the message
	"""
	def addMessage(self, name, MID):
		messageWidget = MessageWidget(name, MID)
		self.messageListWidget.addMessage(messageWidget)
		if self.__subject:
			self.__subject.add(self.__MessageObserver(messageWidget.distributeSignals, MID))
		return messageWidget
		
	"""
	Sets the Selected messageWidget and 

	message messageWidget: the selected MessageWidget object
	"""
	def setSelectedMessage(self, message):
		try:
			self.__matrixObserver.MID = message.MID
		except e:
			print(e)
			self.__matricObserver = self.__MessageObserver(self.__parent.bitMatrix, self._MID)
			self.__subject.add(self.__matricObserver)

	"""
	Adds Signal by name

	parentMessage MessageWidget: the massage widget that this signal is being applied to
	name str: name the the signal
	value int: the inital value of the Signal
	"""
	def addSignal(self, parentMessage, name="Message Label", value=0):
		signalWidget = SignalWidget(name, value)
		parentMessage.addSignal(signalWidget)
		return signalWidget	

