'''
Created on 2013-06-09

@author: Neil
'''

from Controller import Controller

class ZoomController(Controller):
    '''
    classdocs
    '''
    ZOOM_FACTOR = pow(1.5, 0.0625)
    MAX_ZOOM_OUT = 90.0
    
    # Decreases the field of view by ZOOM_FACTOR
    def zoom_in(self):
        self.zoom_by(1.0 / float(self.ZOOM_FACTOR))

    # Increases the field of view by ZOOM_FACTOR
    def zoom_out(self):
        self.zoom_by(self.ZOOM_FACTOR)

    def __set_field_of_view(self, zoom_degrees):
        if not self.enabled:
            return
        self.model.field_of_view = zoom_degrees

    def start(self):
        pass

    def stop(self):
        pass
    
    def zoom_by(self, ratio):
        zoom_degrees = self.model.field_of_view
        zoom_degrees = min(zoom_degrees * ratio, self.MAX_ZOOM_OUT)
        self.__set_field_of_view(zoom_degrees)

    def __init__(self):
        '''
        Constructor
        '''
        Controller.__init__(self)
        