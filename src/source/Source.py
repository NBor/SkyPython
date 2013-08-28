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


Created on 2013-05-16

@author: Neil Borle
'''

from src.units.GeocentricCoordinates import get_instance
from src.utils.Enumeration import enum

update_granularity = enum(Second=0, Minute=1, Hour=2, Day=3, Month=4, Year=5)

class Source(object):
    '''
    Base class for all sources since every source has features such
    as position, color and granularity
    '''

    def __init__(self, new_color, geo_coords=get_instance(0.0, 0.0)):
        '''
        Constructor
        '''
        self.color = new_color
        self.geocentric_coords = geo_coords
        self.granulatriy = None
        self.name_list = []
        
    