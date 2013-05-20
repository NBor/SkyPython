'''
Created on 2013-05-16

@author: Neil
'''

from units.GeocentricCoordinates import get_instance
from utils.Enumeration import enum

update_granularity = enum(Second=0, Minute=1, Hour=2, Day=3, Month=4, Year=5)

class Source(object):
    '''
    classdocs
    '''
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
    