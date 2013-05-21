'''
Created on 2013-05-17

@author: Neil
'''

import math
from utils.Geometry import mod_2_pi, radians_to_degrees

def get_instance(geo_coord=None, earth_coord=None, \
                 planet=None, time=None):
    
    if geo_coord == None and earth_coord == None: 
        raise Exception("must provide geo_coords or helio_coords")
    if geo_coord != None:
        raRad = math.atan2(geo_coord.y, geo_coord.x)
        if (raRad < 0): raRad += math.pi * 2.0
        decRad = math.atan2(geo_coord.z, \
                            math.sqrt(geo_coord.x * geo_coord.x + \
                                      geo_coord.y * geo_coord.y));
                                          
        return RaDec(radians_to_degrees(raRad), radians_to_degrees(decRad))
    else:
        raise NotImplemented("no planet, time")

class RaDec(object):
    '''
    classdocs
    '''
    ra = None
    dec = None

    def to_string(self):
        return "RA: " + self.ra + " degrees\nDec: " + self.dec + " degrees\n"
    
    def calculate_ra_dec_dist(self, helio_coord):
        ra = mod_2_pi(math.atan2(helio_coord.y, helio_coord.x)) * \
        (180.0 / math.pi)
        dec = math.atan(helio_coord.z / \
                        math.sqrt(helio_coord.x * helio_coord.x + \
                                  helio_coord.y * helio_coord.y)) * \
                                  (180.0 / math.pi)

        return RaDec(ra, dec)
    
    def is_circumpolar_for(self, longlat):
        if longlat.latitude > 0.0:
            return self.dec > (90.0 - longlat.latitude)
        else:
            return self.dec < (-90.0 - longlat.latitude)
        
    def is_never_visible(self, longlat):
        if longlat.latitude > 0.0:
            return self.dec < (longlat.latitude - 90.0)
        else:
            return self.dec > (90.0 + longlat.latitude)

    def __init__(self, new_ra, new_dec):
        '''
        Constructor
        '''
        self.ra = new_ra
        self.dec = new_dec
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    from units.LatLong import LatLong
    from units.GeocentricCoordinates import GeocentricCoordinates as GC
    from units.HeliocentricCoordinates import HeliocentricCoordinates as HC
    rd = get_instance(GC(1, 0, 0))
    rd2 = rd.calculate_ra_dec_dist(HC(100, 1, 0, 0))
    print rd2.is_circumpolar_for(LatLong(0, 0))