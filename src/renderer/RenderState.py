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
Created on 2013-05-26

@author: Neil Borle
'''

import math
from src.units.GeocentricCoordinates import GeocentricCoordinates
from src.utils.Matrix4x4 import create_identity

class RenderState(object):
    '''
    Contains all the state necessary for the SkyRenderer
    to render properly.
    '''
    camera_pos = GeocentricCoordinates(0, 0, 0)
    look_dir = GeocentricCoordinates(1, 0, 0)
    up_dir = GeocentricCoordinates(0, 1, 0)
    radius_of_view = 45.0  # in degrees
    up_angle = 0.0
    cos_up_angle = 1.0
    sin_up_angle = 0.0
    screen_width = 480 # originally 100
    screen_height = 800 # originally 100
    transform_to_device = create_identity()
    transform_to_screen = create_identity()
    night_vision_mode = False
    active_sky_region_set = None
    
    def set_camera_pos(self, pos):
        self.camera_pos = pos.copy()
        
    def set_look_dir(self, new_dir):
        self.look_dir = new_dir.copy()
        
    def set_up_dir(self, new_dir):
        self.up_dir = new_dir.copy()
        
    def set_up_angle(self, angle):
        self.up_angle = angle
        self.cos_up_angle = math.cos(angle)
        self.sin_up_angle = math.sin(angle)
        
    def set_screen_size(self, width, height):
        self.screen_width = width
        self.screen_height = height
        
    def set_tranformation_matrices(self, to_device, to_screen):
        self.transform_to_device = to_device
        self.transform_to_screen = to_screen
    
    def __init__(self):
        '''
        Constructor
        '''
        