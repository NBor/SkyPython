'''
// Copyright 2008 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 
// Original Author: Not stated
// 
// Notification of Change: The original java source code has been
// modified in that it has been rewritten in the python programming
// language and additionally, may contain components and ideas that are 
// not found in the original source code.


   Copyright 2013 Neil Borle and Paul Lu

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


Created on 2013-05-19

@author: Neil Borle
'''

import math
from Vector3 import Vector3

def get_instance(orbital_ele=None, planet=None, t_struct=None):
    '''
    Get the location of an object in heliocentric coordinates
    given either an orbital element or a planet.
    '''
    if orbital_ele == None and planet == None: raise Exception("both None")
    
    if orbital_ele == None:
        orbital_ele = planet.get_orbital_elements(t_struct)
        
    anomaly = orbital_ele.get_anomaly()
    ecc = orbital_ele.eccentricity
    radius = orbital_ele.distance * (1 - ecc * ecc) \
        / (1 + ecc * math.cos(anomaly))
    
    per = orbital_ele.perihelion
    asc = orbital_ele.ascending_node
    inc = orbital_ele.inclination
    xh = radius * (math.cos(asc) * math.cos(anomaly + per - asc) - \
                   math.sin(asc) * math.sin(anomaly + per - asc) * \
                   math.cos(inc))
    yh = radius * (math.sin(asc) * math.cos(anomaly + per - asc) + \
                   math.cos(asc) * math.sin(anomaly + per - asc) * \
                   math.cos(inc))
    zh = radius * (math.sin(anomaly + per - asc) * math.sin(inc))
    
    return HeliocentricCoordinates(radius, xh, yh, zh)

class HeliocentricCoordinates(Vector3):
    '''
    Location of an object in heliocentric coordinates
    '''
    OBLIQUITY = 23.439281 * (math.pi / 180.0)
    radius = 0
    
    def subtract(self, helio_coords):
        self.x -= helio_coords.x
        self.y -= helio_coords.y
        self.z -= helio_coords.z
        
    def calculate_equitorial_coords(self):
        return HeliocentricCoordinates(self.radius, self.x, \
        self.y * math.cos(self.OBLIQUITY) - self.z * math.sin(self.OBLIQUITY), \
        self.y * math.sin(self.OBLIQUITY) + self.z * math.cos(self.OBLIQUITY))
        
    def distance_from(self, helio_coord):
        dx = self.x - helio_coord.x
        dy = self.y - helio_coord.y
        dz = self.z - helio_coord.z
        return math.sqrt(dx * dx + dy * dy + dz * dz)
    
    def to_string(self):
        return "({0}, {1}, {2}, {3})".format(self.x, self.y, \
                                             self.z, self.radius)

    def __init__(self, rad, xh, yh, zh):
        '''
        Constructor
        '''
        Vector3.__init__(self, xh, yh, zh)
        self.radius = rad
        
if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    from provider.OrbitalElements import OrbitalElements
    HC = HeliocentricCoordinates(1000, 1, 0, 0)
    HC2 = HC.get_instance(OrbitalElements(54, 0.5, 1, 87, 93, 30))
    print HC2.length()
    