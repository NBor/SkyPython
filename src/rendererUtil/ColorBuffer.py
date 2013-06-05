'''
Created on 2013-06-03

@author: Neil
'''

import numpy as np
from OpenGL import GL
from GLBuffer import GLBuffer

class ColorBuffer(object):
    '''
    classdocs
    '''
    def reset(self, num_verts):
        self.num_vertices = num_verts
        self.regenerate_buffer()
            
    def reload(self):
        self.gl_buffer.reload()
        
    def add_color(self, col=None, a=None, r=None, g=None, b=None):
        if col == None:
            color = ((a & 0xff) << 24) | ((b & 0xff) << 16) | ((g & 0xff) << 8) | (r & 0xff)
            self.color_buffer = np.append(self.color_buffer, [color], 0)
        else:
            self.color_buffer = np.append(self.color_buffer, [col], 0)
    
    def set(self, gl):
        if self.num_vertices == 0:
            return 
        if self.use_vbo and self.gl_buffer.can_use_VBO:
            self.gl_buffer.bind(gl, self.color_buffer, 4*len(self.color_buffer))
            gl.glColorPointer(4, GL.GL_UNSIGNED_BYTE, 0, None)
        else:
            gl.glColorPointer(4, gl.GL_UNSIGNED_BYTE, 0, self.color_buffer)
    
    def regenerate_buffer(self):
        if self.num_vertices == 0:
            return
        self.color_buffer = np.array([], dtype=np.uint32)
            

    def __init__(self, num_verts=0, vbo_bool=False):
        '''
        Constructor
        '''
        self.color_buffer = None
        self.gl_buffer = GLBuffer(GL.GL_ARRAY_BUFFER)
        self.use_vbo = vbo_bool
        self.reset(num_verts)
        