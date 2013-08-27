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
Created on 2013-06-05

@author: Neil Borle
'''

from ColorBuffer import ColorBuffer

class NightVisionBuffer(object):
    '''
    Creates and maintains two instances of color
    buffers, one for night and a regular one. These
    can be switched depending on what is selected.
    '''
    def reset(self, num_verts):
        self.normal_buffer.reset(num_verts)
        self.red_buffer.reset(num_verts)
            
    def reload(self):
        self.normal_buffer.reload()
        self.red_buffer.reload()
        
    def add_color(self, abgr=None, a=None, r=None, g=None, b=None):
        if abgr != None:
            a = int(abgr >> 24) & 0xff
            b = int(abgr >> 16) & 0xff
            g = int(abgr >> 8) & 0xff
            r = int(abgr) & 0xff
        
        self.normal_buffer.add_color(a, r, g, b)
        avg = (r + g + b) / 3
        self.red_buffer.add_color(a, avg, 0, 0)
    
    def set(self, gl, night_vision_mode):
        if night_vision_mode:
            self.red_buffer.set(gl)
        else:
            self.normal_buffer.set(gl)

    def __init__(self, num_verts=0, vbo_bool=False):
        '''
        Constructor
        '''
        self.normal_buffer = ColorBuffer(0, vbo_bool)
        self.red_buffer = ColorBuffer(0, vbo_bool)
        self.reset(num_verts)