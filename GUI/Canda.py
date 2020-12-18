import sys
import multiprocessing
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import Observer
import CandaProcess
import CandaGUIQt 
from random import randint


if __name__ == "__main__":
	#start Process
	process = CandaProcess.ComProcess()
	process.start()

	#Start Qt and add subject to window
	app = QApplication(sys.argv)
	window = CandaGUIQt.MainWindow()
	subject = Observer.ValueUpdateSubject(process.getData(), process.getLock())
	window.messageListWidget.setSubject(subject)
	window.show()

	
	for o in {0x1111, 0x6969, 0xff00}:
		item = window.messageListWidget.addMessage(str(randint(0, 10000000000)), o)
		for i in range(0,9):
			item.addSignal(str(i))

	#start update loop to update the labels
	timer = QTimer()
	timer.timeout.connect(subject.update)
	timer.start(100) #ms

	app.exec_()
	process.kill()
	sys.exit(0)