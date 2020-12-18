from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import randint




class Color(QWidget):
	def __init__(self, color, *args, **kwargs):
		super(Color, self).__init__(*args, **kwargs)

		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)


colors = ['red', 'green', 'blue', 'pink', 'orange', 'black']


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
		self.nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		self.numberLabel = QLabel((f'{number:016x}'))
		self.numberLabel.alignment = Qt.AlignRight
		self.numberLabel.setFont(QFont("Courier New", weight=QFont.Bold))

		hLayout = QHBoxLayout(self)
		hLayout.addSpacing(10)
		hLayout.addWidget(self.nameLabel)
		hLayout.addWidget(self.numberLabel)
		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)

	def setValue(self, value):
		self.numberLabel.setText(f'{value:016x}')

	def setName(self, name):
		self.nameLabel.setText(name)


class MessageWidget(QWidget):
	def __init__(self, name='New Message'):
		super(MessageWidget, self).__init__()
		self.signals = {}
		self.name = QLabel(name)
		#self.name.setFont(QFont("Times", weight=QFont.Bold))
		self.mainLayout = QVBoxLayout()
		self.mainLayout.addWidget(self.name)
		self.setLayout(self.mainLayout)

	def addSignal(self, name="Message Label", number=0):

		signalWidget = SignalWidget(name, number)
		self.mainLayout.addWidget(signalWidget)
		self.signals[name] = signalWidget
		return signalWidget

	def removeSignal(self, name):
		sig = self.signals[name]
		self.mainLayout.remove()
		QWidget.remo

	def distributeSignals(self, value):
		for i in self.signals:
			self.signals[i].setValue(value)


class MessageListWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(MessageListWidget, self).__init__(*args, **kwargs)

		self.messageLayoutBox = QVBoxLayout()
		self.messageLayoutBox.setAlignment(Qt.AlignTop)
		self.messages = dict()

		lw = QWidget()
		lw.setLayout(self.messageLayoutBox)

		sw = QScrollArea()
		# sw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		sw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		sw.setWidgetResizable(True)
		sw.setWidget(lw)

		vLayout = QVBoxLayout()
		vLayout.addWidget(sw)
		self.setLayout(vLayout)

	def addMessage(self, name):
		assert (name not in self.messages.keys()), f'{name}" already exists'
		assert name.strip() != '', "massage name can't be nothing"
		message = MessageWidget(name)
		self.messages[name] = message
		self.messageLayoutBox.addWidget(message)
		return message

	def removeMessage(self, name):
		assert name in self.messages.keys, f'{name}" does not exists'
		assert name.strip() != '', "massage name can't be nothing already exists"
		pass

	def getMessage(self, name):
		assert name in self.messages.keys, f'{name}" does not exists'
		assert name.slice() != '', "massage name can't be nothing already exists"
		return self.messages[name]

	def distributeMessages(self, msgs):
		for i in self.messages:
			self.messages[i].distributeSignals(msgs)


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.updateRate = 10
		self.setWindowTitle("Canda")

		rightZone = QVBoxLayout()
		rightZone.addWidget(SquareBitArray(8, 8))
		rightZone.addWidget(Color('green'))
		rightZoneWidget = QWidget()
		rightZoneWidget.setLayout(rightZone)

		centerZone = Color('blue')

		self.messages = MessageListWidget()
		for o in range(20):
			item = self.messages.addMessage(str(randint(0, 10000000000)))
			for o in range(5):
				item.addSignal(str(randint(0, 10000000000)))

		mainWidget = QSplitter(Qt.Horizontal)
		mainWidget.addWidget(self.messages)
		mainWidget.addWidget(centerZone)
		mainWidget.addWidget(rightZoneWidget)

		self.setCentralWidget(mainWidget)




