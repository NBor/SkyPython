'''
// Copyright 2010 Google Inc.
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
Created on 2013-08-19

@author: Neil Borle
'''

from src.utils.Geometry import radians_to_degrees

class MapMover(object):
    '''
    Responsible for updating the model when dragging, 
    zooming or rotation occurs.
    '''
    
    def on_drag(self, x_pixels, y_pixels):
        pixels_to_rads = self.model.field_of_view / self.size_times_rads_to_degs
        self.control_group.change_up_down(-y_pixels * pixels_to_rads)
        self.control_group.change_right_left(-x_pixels * pixels_to_rads)
        return True
    
    def on_rotate(self, degrees):
        if self.allow_rotation:
            self.control_group.rotate(-degrees)
            return True
        else:
            return False
        
    def on_stretch(self, ratio):
        self.control_group.zoom_by(1.0/ratio)
        return True
    
    def on_shared_preference_change(self, prefs):
        self.allow_rotation = prefs.ALLOW_ROTATION

    def __init__(self, model, controller_group, shared_prefs, screen_height):
        '''
        Constructor
        '''
        
        self.model = model
        self.control_group = controller_group
        self.shared_prefs = shared_prefs
        self.size_times_rads_to_degs = radians_to_degrees(screen_height)
        self.allow_rotation = shared_prefs.ALLOW_ROTATION
        