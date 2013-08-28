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


Created on 2013-06-03

@author: Neil Borle
'''

import numpy as np
from OpenGL import GL
from GLBuffer import GLBuffer

class VertexBuffer(object):
    '''
    Buffers the location of vertices such as stars (points)
    to be loaded into OpenGL. Fixed point is not used in
    PyOpenGL.
    '''
    def reset(self, num_verts):
        self.num_vertices = num_verts
        self.regenerate_buffer()
            
    def reload(self):
        self.gl_buffer.reload()
        
    def add_point(self, vector3):
        #fixed_x = 0xFFFFFFFF & int(vector3.x * 65536.0)
        #fixed_y = 0xFFFFFFFF & int(vector3.y * 65536.0)
        #fixed_z = 0xFFFFFFFF & int(vector3.z * 65536.0)
        #self.vertex_buffer = np.append(self.vertex_buffer, [fixed_x, fixed_y, fixed_z], 0)
        self.vertex_buffer = np.append(self.vertex_buffer, [vector3.z, vector3.y, vector3.x], 0)
    
    def set(self, gl):
        if self.num_vertices == 0:
            return 
        if self.use_vbo and self.gl_buffer.can_use_VBO:
            self.gl_buffer.bind(gl, self.vertex_buffer, 4*len(self.vertex_buffer))
            gl.glVertexPointer(3, gl.GL_FLOAT, 0, None)
        else:
            gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertex_buffer)
    
    def regenerate_buffer(self):
        if self.num_vertices == 0:
            return
        self.vertex_buffer = np.array([], dtype=np.float32)
            

    def __init__(self, num_verts=0, vbo_bool=False):
        '''
        Constructor
        '''
        self.vertex_buffer = None
        self.gl_buffer = GLBuffer(GL.GL_ARRAY_BUFFER)
        self.use_vbo = vbo_bool
        self.reset(num_verts)
        