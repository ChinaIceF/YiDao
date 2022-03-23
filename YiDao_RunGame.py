
import sys
import threading
import time
from PyQt5.QtWidgets import QApplication, QMainWindow
from YiDao_thread_UI import *
from YiDao_thread_Calculate import *

class MyWindow(QMainWindow, Ui_Dialog):

    def __init__(self, parent=None):
    
        super(MyWindow, self).__init__(parent)
        
        self.setupUi(self)



def runCalculateThread(Window):
  
  calculate(Window)


if __name__ == '__main__':
  
    YiDao = QApplication(sys.argv)
    Window = MyWindow()
    thread = threading.Thread(target=runCalculateThread, args=[Window])
    thread.start()
    Window.show()
    sys.exit(YiDao.exec_())

  