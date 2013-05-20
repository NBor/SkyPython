'''
Created on 2013-05-16

@author: Neil
'''

from Source import Source

class TextSource(Source):
    '''
    classdocs
    '''


    def __init__(self, new_label, color, geo_coords, new_offset=0.02, new_fontsize=15):
        '''
        Constructor
        '''
        Source.__init__(self, color, geo_coords)
        self.label = new_label
        self.offset = new_offset
        self.font_size = new_fontsize
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''