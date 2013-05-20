'''
Created on 2013-05-16

@author: Neil
'''

from units.GeocentricCoordinates import get_instance

def enum(**enums):
    return type('Enum', (), enums)

class Source(object):
    '''
    classdocs
    '''
    update_granularity = enum(Second=0, Minute=1, Hour=2, Day=3, Month=4, Year=5)
    granulatriy = None
    color = None
    geocentric_coords = None
    name_list = []


    def __init__(self, new_color, geo_coords=get_instance(0.0, 0.0)):
        '''
        Constructor
        '''
        self.color = new_color
        self.geocentric_coords = geo_coords
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    