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



Created on 2013-08-29

@author: Neil
'''

from Controller import Controller
from units.LatLong import LatLong

class LocationController(Controller):
    '''
    Sets the AstronomerModel's position in terms of 
    latitude and longitude.
    '''
    
    class LocationProvider(object):
        '''
        Get the location from a phone or from a config file
        '''
        FROM_FILE = True
        
        def get_lat_long(self):
            if self.FROM_FILE:
                return self.lat_long_from_file()
            else:
                # have not tested with a phone
                raise NotImplementedError
            
        def lat_long_from_file(self):
            with open("assets/LatitudeLongitudeConfig.txt", 'r') as f:
                for line in f.readlines():
                    if not line.startswith('#'):
                        lat, lon = line.split(',')
                return LatLong(float(lat), float(lon))
        
        def __init__(self, force_gps):
            self.force_gps = force_gps
    
    # Must match the key in the preferences file.
    NO_AUTO_LOCATE = "no_auto_locate"
    # Must match the key in the preferences file.
    FORCE_GPS = "force_gps"
    MINIMUM_DISTANCE_BEFORE_UPDATE_METRES = 2000
    LOCATION_UPDATE_TIME_MILLISECONDS = 600000
    MIN_DIST_TO_SHOW_TOAST_DEGS = 0.01

    def start(self):
        no_auto_locate = self.shared_prefs.PREFERENCES[self.NO_AUTO_LOCATE]
        force_gps = self.shared_prefs.PREFERENCES[self.FORCE_GPS]
        
        if no_auto_locate:
            self.set_location_from_prefs()
        else:
            location_provider = self.LocationProvider(force_gps)
            self.set_location_in_model(location_provider.get_lat_long())
    
    def set_location_in_model(self, lat_long):
        self.model.set_location(lat_long)
    
    def set_location_from_prefs(self):
        lat, lon = self.shared_prefs.LATITUDE, self.shared_prefs.LONGITUDE
        self.set_location_in_model(LatLong(lat, lon))
    
    def stop(self):
        # do nothing
        pass
    
    def on_location_change(self):
        raise NotImplementedError

    def __init__(self, prefs):
        '''
        Constructor
        '''
        Controller.__init__(self)
        self.shared_prefs = prefs
        