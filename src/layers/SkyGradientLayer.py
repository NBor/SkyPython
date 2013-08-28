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
// Original Author: John Taylor, Brent Bryan
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


Created on 2013-06-17

@author: Neil Borle
'''

import threading
import calendar
from src.base.TimeConstants import MILLISECONDS_PER_MINUTE
from src.provider.SolarPositionCalculator import get_solar_position
from src.units.GeocentricCoordinates import get_instance

class SkyGradientLayer(object):
    '''
    updates the position of the sky gradient.
    '''
    renderer_lock = threading.RLock()
    UPDATE_FREQUENCY_MS = 5 * MILLISECONDS_PER_MINUTE
    
    def initialize(self):
        # Do Nothing
        pass
    
    def register_with_renderer(self, rend_controller):
        self.controller = rend_controller
        self.redraw()
    
    def set_visible(self, visible):
        if visible:
            self.redraw()
        else:
            with self.renderer_lock:
                self.controller.queue_disable_sky_gradient()
    
    def redraw(self):
        '''
        Redraws the sky shading gradient using the model's current time.
        '''
        model_time = self.model.get_time()
        Ms_since_epoch = calendar.timegm(model_time) * 100
        
        if abs(Ms_since_epoch - self.last_update_time_Ms) > self.UPDATE_FREQUENCY_MS:
            self.last_update_time_Ms = Ms_since_epoch
            
            sun_pos = get_solar_position(model_time)
            
            with self.renderer_lock:
                gc = get_instance(sun_pos.ra, sun_pos.dec)
                self.controller.queue_enable_sky_gradient(gc)
    
    def get_layer_id(self):
        return 0
    
    def get_layer_name(self):
        return "Sky Gradient"
    
    def get_preference_id(self):
        return "source_provider.8"
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def search_by_object_name(self, name):
        return []
    
    def get_object_names_matching_prefix(self, prefix):
        return set()


    def __init__(self, model):
        '''
        Constructor
        '''
        self.model = model
        self.controller = None
        self.last_update_time_Ms = 0
        
        
        