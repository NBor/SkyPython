'''
Created on 2013-06-02

@author: Neil
'''

from numpy import array_equal, empty_like

class GLBuffer(object):
    '''
    classdocs
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
            
            #print self.buffer_id
            if self.buffer_id == -1:
                self.buffer_id = gl.glGenBuffers(1)
            #print self.buffer_id
            #print self.buffer_size, len(self.buffer)
            #print self.buffer_type
            
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