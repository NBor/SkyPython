'''
Created on 2013-05-16

@author: Neil
'''

from Source import Source
from utils.Colors import colors

class LineSource(Source):
    '''
    classdocs
    '''

    def __init__(self, gcvs, new_color=colors.WHITE, lw=1.5):
        '''
        Constructor
        '''
        Source.__init__(self, new_color)
        self.ra_decs = []
        self.line_width = lw
        self.gc_verticies = gcvs
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''