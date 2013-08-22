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
Created on 2013-06-03

@author: Neil Borle
'''

import numpy as np
from OpenGL import GL
from GLBuffer import GLBuffer

class IndexBuffer(object):
    '''
    classdocs
    '''
    def reset(self, num_inds):
        self.num_indices = num_inds
        self.regenerate_buffer()
            
    def reload(self):
        self.gl_buffer.reload()
        
    def add_index(self, index):
        self.index_buffer = np.append(self.index_buffer, [index], 0)
    
    def regenerate_buffer(self):
        if self.num_indices == 0:
            return
        self.index_buffer = np.array([], dtype=np.ushort)
        
    def draw(self, gl, primitive_type):
        if self.num_indices == 0:
            return 
        if self.use_vbo and self.gl_buffer.can_use_VBO:
            self.gl_buffer.bind(gl, self.index_buffer, 2*len(self.index_buffer))
            gl.glDrawElements(primitive_type, self.num_indices, gl.GL_UNSIGNED_SHORT, None)
            self.gl_buffer.unbind(gl)
        else:
            gl.glDrawElements(primitive_type, self.num_indices, 
                              gl.GL_UNSIGNED_SHORT, self.index_buffer)

    def __init__(self, num_inds=0, vbo_bool=False):
        '''
        Constructor
        '''
        self.index_buffer = None
        self.gl_buffer = GLBuffer(GL.GL_ELEMENT_ARRAY_BUFFER)
        self.use_vbo = vbo_bool
        self.reset(num_inds)
        