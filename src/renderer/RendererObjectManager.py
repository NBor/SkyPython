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

import threading
from src.utils.Enumeration import enum

class RendererObjectManager(object):
    '''
    ABSTRACT CLASS DO NOT DIRECTLY INSTANTIATE
    Abstracts the commonality between all the 
    object managers. Chiefly important attributes.
    '''
    lock = threading.RLock()
    max_radius_of_view = 360   # in degrees
    # Used to distinguish between different renderers, so we can have sets of them.
    s_index = 0

    update_type = enum(Reset=0, UpdatePositions=1, UpdateImages=2)
    
    def compare_to(self, render_object_manager):
        raise NotImplementedError("Not implemented")
    
    def draw(self, gl):
        if self.enabled and self.render_state.radius_of_view <= self.max_radius_of_view:
            self.draw_internal(gl)
            
    def queue_for_reload(self, bool_full_reload):
        self.listener(self, bool_full_reload)

    def __init__(self, new_layer, new_texture_manager):
        '''
        Constructor
        '''
        self.layer = new_layer
        self.texture_manager = new_texture_manager
        self.enabled = True
        self.render_state = None
        self.listener = None
        with self.lock:
            self.index = self.s_index + 1