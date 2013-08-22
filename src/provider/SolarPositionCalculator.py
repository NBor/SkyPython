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
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-06-17

@author: Neil Borle
'''

from src.provider.Planet import Planet, planet_enum, res
from src.units.RaDec import get_instance as radec_get_instance
from src.units.HeliocentricCoordinates import get_instance as hc_get_instance

def get_solar_position(time):
    '''
    # Calculates the position of the Sun in Ra and Dec
    '''
    sun = Planet(planet_enum.SUN, res[planet_enum.SUN][0], 
                 res[planet_enum.SUN][1], res[planet_enum.SUN][2])
    sun_coords = hc_get_instance(None, sun, time)
    
    ra_dec = radec_get_instance(None, sun_coords, sun, time)
    return ra_dec

