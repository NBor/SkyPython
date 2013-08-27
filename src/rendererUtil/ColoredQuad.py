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
Created on 2013-06-19

@author: Neil Borle
'''

from VertexBuffer import VertexBuffer
from src.units.Vector3 import Vector3

class ColoredQuad(object):
    '''
    Provides an abstraction so that colored rectangles
    can be buffered and loaded into OpenGL
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
        
        