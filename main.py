'''
Created on 2013-05-14

@author: Neil
'''

import sys
from PySide.QtGui import QApplication

from skypython.SkyPython import SkyPython

def start_application():
    
    app = QApplication(sys.argv)
    w = SkyPython()
    w.show()
    app.installEventFilter(w)
    app.exec_()

if __name__ == '__main__':
    start_application()
    
    