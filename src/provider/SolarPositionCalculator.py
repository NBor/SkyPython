'''
Created on 2013-06-17

@author: Neil
'''

from units.RaDec import get_instance
from units.HeliocentricCoordinates import get_instance as helio_get_instance

# Calculate the position of the Sun in RA and Dec
def get_solar_position(time):
    #sun_coordinates = helio_get_instance(Planet.Sun, time)
    #ra_dec = getInstance(Planet.Sun, time, sun_coordinates)
    from units.GeocentricCoordinates import GeocentricCoordinates as GC
    ra_dec = get_instance(GC(0, 0, 0))
    return ra_dec

