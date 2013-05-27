'''
Created on 2013-05-16

@author: Neil
'''

import math
from Vector3 import Vector3

def get_instance(ra, dec):
    coords = GeocentricCoordinates(0.0, 0.0, 0.0)
    coords.update_from_ra_dec(ra, dec)
    return coords

def get_instance_from_list(l):
    return GeocentricCoordinates(l[0], l[1], l[2])

def get_instance_from_vector3(v3):
    return GeocentricCoordinates(v3.x, v3.y, v3.z)

class GeocentricCoordinates(Vector3):
    '''
    classdocs
    '''

    def update_from_ra_dec(self, ra, dec):
        ra_radians = ra * (math.pi / 180.0)
        dec_radians = dec * (math.pi / 180.0)
        
        self.x = math.cos(ra_radians) * math.cos(dec_radians)
        self.y = math.sin(ra_radians) * math.cos(dec_radians)
        self.z = math.sin(dec_radians)
    
    def update_from_list(self, l):
        self.x = l[0]
        self.y = l[1]
        self.z = l[2]
        
    def copy(self):
        return GeocentricCoordinates(self.x, self.y, self.z)

    def __init__(self, new_x, new_y, new_z):
        '''
        Constructor
        '''
        Vector3.__init__(self, new_x, new_y, new_z)
        
if __name__ == "__main__":
    '''
    For debugging purposes
    ready for testing
    '''
    GC = GeocentricCoordinates(4.0, 5.0, 0.0)
    print GC.x, GC.y, GC.z
    GC.assign(vector3=Vector3(1.0, 3.0, 5.0))
    print GC.to_float_array()
    