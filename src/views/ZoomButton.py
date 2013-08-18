'''
Created on 2013-08-18

@author: Neil
'''

import PySide.QtCore as QtCore
import ZoomWidget
from PySide.QtGui import QWidget

class ZoomButton(QWidget, ZoomWidget.Ui_ZoomBar):
    '''
    classdocs
    '''
    
    def __init__(self, parent=None):
        '''
        create ZoomButtons instance
        '''
        super(ZoomButton, self).__init__(parent)
        self.setupUi(ZoomButton)
        
    def checkForButtonPress(self, source, event, controller):
        
        if event.type() != QtCore.QEvent.MouseButtonPress:
            return False
        
        if source == self.ZoomIn:
            controller.zoom_in()
            return True
        
        elif source == self.ZoomOut:
            controller.zoom_out()
            return True
            
        else:
            return False
        