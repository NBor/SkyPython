'''
Created on 2013-05-16

@author: Neil
'''

from Source import Source
from utils.Colors import colors

class AstronomicalSource(Source):
    '''
    classdocs
    '''
    level = None
    names = []
    image_sources = []
    line_sources = []
    point_sources = []
    text_sources = []
            
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
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    new = AstronomicalSource()
    print new.point_sources