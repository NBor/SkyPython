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


Created on 2013-05-17

@author: Neil Borle
'''

import math
import GeocentricCoordinates as GC
from src.utils.Geometry import cosine_similarity, radians_to_degrees

class LatLong(object):
    '''
    Basic class that contains a latitude and a longitude
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
    '''
    A = LatLong(20, 4)
    B = LatLong(16, 9)
    print A.distance_from(B)