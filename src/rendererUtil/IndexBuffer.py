'''
Created on 2013-06-03

@author: Neil
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
        