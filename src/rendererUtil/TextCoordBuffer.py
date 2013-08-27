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

class TextCoordBuffer(object):
    '''
    Buffers text coordinates, the rectangles that hold the
    text, so that they can be loaded into OpenGL. Fixed point
    buffering is not available in PyOpenGL.
    '''
    def reset(self, num_verts):
        if num_verts < 0:
            num_verts = 0
            
        self.num_vertices = num_verts
        self.regenerate_buffer()
            
    def reload(self):
        self.gl_buffer.reload()
        
    def add_text_coord(self, u, v):
        #fixed_u = 0xFFFFFFFF & int(u * 65536.0)
        #fixed_v = 0xFFFFFFFF & int(v * 65536.0)
        #self.text_coord_buffer = np.append(self.text_coord_buffer, [fixed_u, fixed_v], 0)
        self.text_coord_buffer = np.append(self.text_coord_buffer, [u, v], 0)
    
    def set(self, gl):
        if self.num_vertices == 0:
            return 
        if self.use_vbo and self.gl_buffer.can_use_VBO:
            self.gl_buffer.bind(gl, self.text_coord_buffer, self.num_vertices)
            gl.glTexCoordPointer(2, gl.GL_FLOAT, 0, 0)
        else:
            gl.glTexCoordPointer(2, gl.GL_FLOAT, 0, self.text_coord_buffer)
    
    def regenerate_buffer(self):
        if self.num_vertices == 0:
            return
        self.text_coord_buffer = np.array([], dtype=np.float32)
            

    def __init__(self, num_verts=0, vbo_bool=False): 
        '''
        Constructor
        '''
        self.text_coord_buffer = None
        self.gl_buffer = GLBuffer(GL.GL_ARRAY_BUFFER)
        self.use_vbo = vbo_bool
        self.reset(num_verts)
        