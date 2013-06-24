'''
Created on 2013-05-16

@author: Neil
'''

from Source import Source
from units.GeocentricCoordinates import get_instance

class TextSource(Source):
    '''
    classdocs
    '''


    def __init__(self, new_label, color, geo_coords=get_instance(0.0, 0.0), \
                 new_offset=0.02, new_fontsize=15):
        '''
        Constructor
        '''
        Source.__init__(self, color, geo_coords)
        print hex(color)
        self.label = new_label
        self.offset = new_offset
        self.font_size = new_fontsize
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    T = TextSource("Sun", 0xFA783B90)
    print T.geocentric_coords.z