'''
Created on 2013-05-17

@author: Neil
'''

import math
import GeocentricCoordinates as GC
from utils.Geometry import cosine_similarity, radians_to_degrees

class LatLong(object):
    '''
    classdocs
    '''
    latitude = None
    longitude = None
    
    def distance_from(self, lat_long):
        other_point = GC.get_instance(lat_long.longitude, lat_long.latitude)
        this_point = GC.get_instance(self.longitude, self.latitude)
        cos_Theta = cosine_similarity(this_point, other_point)
        return radians_to_degrees(math.acos(cos_Theta))

    def __init__(self, new_lat, new_long):
        '''
        Constructor
        '''
        self.latitude = new_lat
        self.longitude = new_long

if __name__ == "__main__":
    '''
    for debugging purposes
    Ready for testing
    '''
    A = LatLong(20, 4)
    B = LatLong(16, 9)
    print A.distance_from(B)