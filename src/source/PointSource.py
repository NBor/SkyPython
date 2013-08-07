'''
Created on 2013-05-16

@author: Neil
'''

from Source import Source
from src.utils.Enumeration import enum
from src.units.GeocentricCoordinates import get_instance

shape_enum = enum(CIRCLE=0, STAR=1, ELLIPTICAL_GALAXY=2, \
                      SPIRAL_GALAXY=3, IRREGULAR_GALAXY=4, \
                      LENTICULAR_GALAXY=3, GLOBULAR_CLUSTER=5, \
                      OPEN_CLUSTER=6, NEBULA=7, HUBBLE_DEEP_FIELD=8)

class PointSource(Source):
    '''
    classdocs
    '''

    def __init__(self, new_color, new_size, geo_coords=get_instance(0.0, 0.0), \
                 new_shape=shape_enum.CIRCLE):
        '''
        Constructor
        '''
        Source.__init__(self, new_color, geo_coords)
        self.size = new_size
        self.point_shape = new_shape
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    P = PointSource(0xF0F73615, 1)
    print P.point_shape
    print P.geocentric_coords.x