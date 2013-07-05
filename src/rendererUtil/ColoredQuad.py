'''
Created on 2013-06-19

@author: Neil
'''

from VertexBuffer import VertexBuffer
from ..units.Vector3 import Vector3

class ColoredQuad(object):
    '''
    classdocs
    '''
    def draw(self, gl):
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
    
        # Enable blending if alpha != 1.
        if self.a != 1:
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        gl.glDisable(gl.GL_TEXTURE_2D)
        
        self.position.set(gl)
        gl.glColor4f(self.r, self.g, self.b, self.a)
        
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
        
        gl.glEnable(gl.GL_TEXTURE_2D)
    
        # Disable blending if alpha != 1.
        if self.a != 1:
            gl.glDisable(gl.GL_BLEND)

    def __init__(self, r, g, b, a,
                 px, py, pz,
                 ux, uy, uz,
                 vx, vy, vz):
        '''
        Constructor
        '''
        self.position = VertexBuffer(12)
        
        # Upper left
        self.position.add_point(Vector3(px - ux - vx, py - uy - vy, pz - uz - vz))
        
        # upper left
        self.position.add_point(Vector3(px - ux + vx, py - uy + vy, pz - uz + vz))
        
        # lower right
        self.position.add_point(Vector3(px + ux - vx, py + uy - vy, pz + uz - vz))
        
        # upper right
        self.position.add_point(Vector3(px + ux + vx, py + uy + vy, pz + uz + vz))
    
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        
        