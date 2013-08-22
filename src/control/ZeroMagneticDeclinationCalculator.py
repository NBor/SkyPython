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

class ZeroMagneticDeclinationCalculator(object):
    '''
    This is a dummy class that provides a magnetic
    declination of 0.
    '''
    def get_declination(self):
        return 0
    
    def set_location_and_time(self, lat_long, time_in_mills):
        pass #Do Nothing
    
    def to_string(self):
        return "Zero Magnetic Correction"    

    def __init__(self):
        '''
        Constructor
        '''
        