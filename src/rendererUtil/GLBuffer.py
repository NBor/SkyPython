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
// Original Author: James Powell
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-06-02

@author: Neil Borle
'''

from numpy import array_equal, empty_like

class GLBuffer(object):
    '''
    Buffer for OpenGL which encapsulates the buffer
    binding and unbinding.
    '''
    can_use_VBO = False
    
    def unbind(self, gl):
        if self.can_use_VBO:
            gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
            gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
    
    def bind(self, gl, m_buffer, m_buff_size):
        if self.can_use_VBO:
            self.maybe_regen_buffer(gl, m_buffer, m_buff_size)
            gl.glBindBuffer(self.buffer_type, self.buffer_id)
        else:
            raise Exception("Cannot use VBOs")

    def reload(self):
        # Just reset all of the values so we'll reload on the next call
        # to maybeRegenerateBuffer.
        self.buffer = None
        self.buffer_size = 0
        self.buffer_id = -1
        
    def maybe_regen_buffer(self, gl, m_buffer, m_buff_size):
        if not array_equal(self.buffer, m_buffer) or self.buffer_size != m_buff_size:
            self.buffer = empty_like(m_buffer)
            self.buffer = m_buffer[:]
            self.buffer_size = m_buff_size
            
            if self.buffer_id == -1:
                self.buffer_id = gl.glGenBuffers(1)
            
            gl.glBindBuffer(self.buffer_type, self.buffer_id)
            gl.glBufferData(self.buffer_type, m_buff_size, m_buffer, gl.GL_STATIC_DRAW)

    def __init__(self, b_type):
        '''
        Constructor
        '''
        self.buffer = None
        self.buffer_size = 0
        self.buffer_id = -1
        self.buffer_type = b_type