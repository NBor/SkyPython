'''
Created on 2013-06-17

@author: Neil
'''

from src.provider.Planet import Planet, planet_enum, res
from src.units.RaDec import get_instance as radec_get_instance
from src.units.HeliocentricCoordinates import get_instance as hc_get_instance

# Calculate the position of the Sun in RA and Dec
def get_solar_position(time):
    sun = Planet(planet_enum.SUN, res[planet_enum.SUN][0], 
                 res[planet_enum.SUN][1], res[planet_enum.SUN][2])
    sun_coords = hc_get_instance(None, sun, time)
    
    ra_dec = radec_get_instance(None, sun_coords, sun, time)
    return ra_dec

