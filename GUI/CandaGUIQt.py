from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from random import randint
import sys


class Color(QWidget):
	def __init__(self, color, *args, **kwargs):
		super(Color, self).__init__(*args, **kwargs)

		self.setAutoFillBackground(True)

		palette = self.palette()
		palette.setColor(QPalette.Window, QColor(color))
		self.setPalette(palette)


colors = ['red', 'green', 'blue', 'pink', 'orange', 'black']


class SignalLabel(QWidget):
	def __init__(self, name="Message Label", number=0):
		super(SignalLabel, self).__init__()
		self.setAutoFillBackground(True)
		palette = self.palette()
		palette.setColor(QPalette.Window, QColor('red'))
		self.setPalette(palette)
		hLayout = QHBoxLayout(self)
		nameLabel = QLabel(str(name))
		nameLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
		numberLabel = QLabel((f'{number:016x}'))
		numberLabel.alignment = Qt.AlignRight

		hLayout.addWidget(nameLabel)
		hLayout.addWidget(numberLabel)
		self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)


class MessageWidget(QWidget):

	def __init__(self, name='New Message'):
		super(MessageWidget, self).__init__()
		self.signals = {}
		self.mainLayout = QVBoxLayout()

		self.name = QLabel(name)
		self.name.setFont(QFont("Times", weight=QFont.Bold))
		self.mainLayout.addWidget(self.name)
		self.setLayout(self.mainLayout)

	def addSignal(self, name="Message Label", number=0):
		hLayout = QHBoxLayout()
		hLayout.addSpacing(10)
		print(name)
		signalWidget = SignalLabel(name, number)
		hLayout.addWidget(signalWidget)
		self.mainLayout.addLayout(hLayout)
		self.signals[name] = signalWidget
		return signalWidget


class MessageListWidget(QWidget):
	def __init__(self, *args, **kwargs):
		super(MessageListWidget, self).__init__(*args, **kwargs)

		ll = QVBoxLayout()
		ll.setAlignment(Qt.AlignTop)

		for n in range(5):
			mw = MessageWidget()
			for i in colors:
				mw.addSignal(i, randint(0, 0xffffffffffffffff))
			ll.addWidget(mw)

		lw = QWidget()
		lw.setLayout(ll)

		sw = QScrollArea()
		sw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
		sw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		sw.setWidgetResizable(True)
		sw.setWidget(lw)

		vLayout = QVBoxLayout()
		vLayout.addWidget(sw)
		self.setLayout(vLayout)


class MainWindow(QMainWindow):
	def __init__(self, *args, **kwargs):
		super(MainWindow, self).__init__(*args, **kwargs)

		self.setWindowTitle("Canda")

		sl = QVBoxLayout()

		sl.addWidget(Color('yellow'))
		sl.addWidget(Color('pink'))

		ml = QGridLayout()
		ml.addWidget(MessageListWidget(), 0, 0)
		n = Color('blue')
		n.setMinimumWidth(100)
		ml.addWidget(n, 0, 1)
		ml.addLayout(sl, 0, 2)

		cental = QWidget()
		cental.setLayout(ml)

		self.setCentralWidget(cental)


app = QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec_()
