'''
Created on 2013-05-16

@author: Neil
'''

from Source import Source
from src.utils.Colors import colors

class AstronomicalSource(Source):
    '''
    classdocs
    '''
            
    def add_image(self, image):
        self.image_sources.append(image)
        
    def add_line(self, line):
        self.line_sources.append(line)
        
    def add_point(self, point):
        self.point_sources.append(point)
        
    def add_label(self, label):
        self.text_sources.append(label)

    def __init__(self, new_color=colors.WHITE):
        '''
        Constructor
        '''
        Source.__init__(self, new_color)
        self.level = None
        self.names = []
        self.image_sources = []
        self.line_sources = []
        self.point_sources = []
        self.text_sources = []
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    new = AstronomicalSource()
    print new.point_sources