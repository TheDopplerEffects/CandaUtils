import sys
import multiprocessing
import CandaProcess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import CandaGUIQt 


if __name__ == "__main__":
	app = QApplication(sys.argv)
	window = CandaGUIQt.MainWindow()

	manager = multiprocessing.Manager()
	data = manager.list([0, 0])
	lock = multiprocessing.Lock()
	process = multiprocessing.Process(target=CandaProcess.updateLoop, args=[data, lock])
	process.start()

	subject = ValueUpdateSubject(data, lock)
	subject.add(window.messages.distributeMessages)
	subject.update()

	window.show()

	timer = QTimer()
	timer.timeout.connect(subject.update)
	timer.start(100)

	app.exec_()
	process.kill()
	sys.exit()