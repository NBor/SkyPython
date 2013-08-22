'''
// Copyright 2009 Google Inc.
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
// Original Author: John Taylor
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-23

@author: Neil Borle
'''

class RealMagneticDeclinationCalculator(object):
    '''
    This class provides an interface to access data from
    phone hardware to obtain magnetic declination.
    
    This class in not functional
    '''
    geo_magnetic_field = None
    
    def get_declination(self):
        if self.geo_magnetic_field == None:
            return 0
        else:
            raise NotImplementedError("Not implemented")
    
    def set_location_and_time(self, lat_long, time_in_mills):
        self.geo_magnetic_field = None # change this
        raise NotImplementedError("Not implemented yet")
    
    def to_string(self):
        return "Real Magnetic Correction"

    def __init__(self):
        '''
        Constructor
        '''
        