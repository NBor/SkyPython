'''
Created on 2013-05-17

@author: Neil
'''

import math
from units.HeliocentricCoordinates import HeliocentricCoordinates, get_instance as hc_get_instance
from utils.Geometry import mod_2_pi, radians_to_degrees
from utils.Enumeration import enum

planet_enum = enum(MERCURY=0, VENUS=1, SUN=2, MARS=3, 
              JUPITER=4, SATURN=5, URANUS=6, 
              NEPTUNE=7, PLUTO=8, MOON=9)

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
        if planet.id == planet_enum.MOON:
            return planet.calculate_lunar_geocentric_location(time)
            
        coords = None
        if planet.id == planet_enum.SUN:
            # Invert the view, since we want the Sun in earth coordinates, not the Earth in sun
            # coordinates.
            coords = HeliocentricCoordinates(earth_coord.radius, earth_coord.x * -1.0, 
                                             earth_coord.y * -1.0, earth_coord.z * -1.0)
        else:
            coords = hc_get_instance(None, planet, time)
            coords.subtract(earth_coord)
            
        equ = coords.calculate_equitorial_coords()
        return calculate_ra_dec_dist(equ)
    
def calculate_ra_dec_dist(helio_coord):
    ra = mod_2_pi(math.atan2(helio_coord.y, helio_coord.x)) * \
    (180.0 / math.pi)
    dec = math.atan(helio_coord.z / \
                    math.sqrt(helio_coord.x * helio_coord.x + \
                              helio_coord.y * helio_coord.y)) * \
                              (180.0 / math.pi)
                                
    return RaDec(ra, dec)

class RaDec(object):
    '''
    classdocs
    '''
    ra = None
    dec = None

    def to_string(self):
        return "RA: " + self.ra + " degrees\nDec: " + self.dec + " degrees\n"
    
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