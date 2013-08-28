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
// Original Author: Kevin Serafini, Brent Bryan
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


Created on 2013-05-20

@author: Neil Borle
'''
import math
from src.utils.Geometry import mod_2_pi

class OrbitalElements(object):
    '''
    This class wraps the six parameters which define the path an object takes as
    it orbits the sun.
    
    The equations come from JPL's Solar System Dynamics site:
    http://ssd.jpl.nasa.gov/?planet_pos
    
    The original source for the calculations is based on the approximations described in:
    Van Flandern T. C., Pulkkinen, K. F. (1979): "Low-Precision Formulae for
    Planetary Positions", 1979, Astrophysical Journal Supplement Series, Vol. 41,
    pp. 391-411.
    '''
    EPSILON = 1.0e-6
    
    distance = None         #Mean distance (AU)
    eccentricity = None     #Eccentricity of orbit
    inclination = None      #Inclination of orbit (AngleUtils.RADIANS)
    ascending_node = None   #Longitude of ascending node (AngleUtils.RADIANS)
    perihelion = None       #Longitude of perihelion (AngleUtils.RADIANS)
    mean_longitude= None    #Mean longitude (AngleUtils.RADIANS)

    def get_anomaly(self):
        '''
        compute anomaly using mean anomaly and eccentricity
        returns value in radians
        '''
        m = self.mean_longitude - self.perihelion 
        e = self.eccentricity

        e0 = m + e * math.sin(m) * (1.0 + e * math.cos(m))
        
        counter = 0
        while(counter <= 100):
            e1 = e0
            e0 = e1 - (e1 - e * math.sin(e1) - m) / (1.0 - e * math.cos(e1))
            if math.fabs(e0 - e1) > self.EPSILON:
                break
            counter += 1
            
        v = 2.0 * math.atan(math.sqrt((1 + e) / (1 - e)) * math.tan(0.5 * e0))
        return mod_2_pi(v)
            
    def to_string(self):
        l = []
        l.append("Mean Distance: " + str(self.distance) + " (AU)\n");
        l.append("Eccentricity: " + str(self.eccentricity) + "\n");
        l.append("Inclination: " + str(self.inclination) + " (AngleUtils.RADIANS)\n");
        l.append("Ascending Node: " + str(self.ascending_node) + " (AngleUtils.RADIANS)\n");
        l.append("Perihelion: " + str(self.perihelion) + " (AngleUtils.RADIANS)\n");
        l.append("Mean Longitude: " + str(self.mean_longitude) + " (AngleUtils.RADIANS)\n");

        return ''.join(l)

    def __init__(self, d, e, i, a, p, l):
        '''
        Constructor
        '''
        self.distance = d
        self.eccentricity = e
        self.inclination = i
        self.ascending_node = a
        self.perihelion = p
        self.mean_longitude = l
        
if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    OE = OrbitalElements(54, 0.5, 1, 87, 93, 30)
    print OE.get_anomaly()