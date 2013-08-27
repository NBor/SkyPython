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
// Original Author: Brent Bryan
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-16

@author: Neil Borle
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
    This class represents a astronomical point source, 
    such as a star, or a distant galaxy.
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
    '''
    P = PointSource(0xF0F73615, 1)
    print P.point_shape
    print P.geocentric_coords.x