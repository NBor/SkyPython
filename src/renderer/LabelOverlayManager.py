'''
// Copyright 2009 Google Inc.
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


Created on 2013-07-26

@author: Neil Borle
'''

from src.rendererUtil.LabelMaker import LabelMaker
from src.rendererUtil.IndexBuffer import IndexBuffer
from src.rendererUtil.VertexBuffer import VertexBuffer

class LabelOverlayManager(object):
    '''
    Manages rendering of which appears at fixed points on the screen, rather
    than text which appears at fixed points in the world.
    '''
    class Label(LabelMaker.LabelData):
        '''
        Holds state on a single label
        '''
        
        def __init__(self, text, color, size):
            '''
            constructor
            '''
            LabelMaker.LabelData.__init__(self, text, color, size)
            self.enabled = True
            self.x, self.y = 0, 0
            self.alpha = 1.0

    def initialize(self, gl, render_state, labels, texture_manager):
        self.labels = labels[:] # deep copy
        self.texture = self.label_maker.initialize(gl, render_state, self.labels, texture_manager)
        
    def release_textures(self, gl):
        if self.texture != None:
            self.texture.shutdown(gl)
            self.texture = None
            
    def draw(self, gl, screen_width, screen_height):
        if self.texture == None or self.labels == []:
            return
        
        gl.glEnable(gl.GL_TEXTURE_2D)
        self.texture.bind(gl)
        
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        gl.glTexEnvx(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, 
                     gl.GL_MODULATE)
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        
        # Change to orthographic projection, where the units in model view space
        # are the same as in screen space.
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrthof(0, screen_width, 0, screen_height, -100, 100)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        
        for label in self.labels:
            if label.enabled:
                x = label.x - label.width_in_pixels / 2
                y = label.y
                
                gl.glLoadIdentity()
                
                # Move the label to the correct offset.
                gl.glTranslatef(x, y, 0.0)
                
                # Scale the label to the correct size.
                gl.glScalef(label.width_in_pixels, label.height_in_pixels, 0.0)
                
                # Set the alpha for the label.
                gl.glColor4f(1, 1, 1, label.getAlpha())
                
                # Draw the label.
                self.vertex_buffer.set(gl)
                gl.glTexCoordPointer(2, gl.GL_FIXED, 0, label.tex_coords)
                self.index_buffer.draw(gl, gl.GL_TRIANGLES)
                
        # Restore the old matrices.
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
        
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_REPLACE)
        gl.glDisable(gl.GL_BLEND)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        
        gl.glDisable(gl.GL_TEXTURE_2D)

    def __init__(self):
        '''
        Constructor
        '''
        self.labels = []
        self.label_maker = LabelMaker(True)
        self.texture = None
        self.vertex_buffer = VertexBuffer(4, False)
        self.index_buffer = IndexBuffer(6)
        #private Paint mLabelPaint = new Paint();
        #mLabelPaint.setAntiAlias(true);
        
        self.vertex_buffer.add_point(0, 0, 0)  # Bottom left
        self.vertex_buffer.add_point(0, 1, 0)  # Top left
        self.vertex_buffer.add_point(1, 0, 0)  # Bottom right
        self.vertex_buffer.add_point(1, 1, 0)  # Top right
        
        # Triangle one: bottom left, top left, bottom right.  
        self.index_buffer.add_index(0)
        self.index_buffer.add_index(1)
        self.index_buffer.add_index(2)
        
        # Triangle two: bottom right, top left, top right.
        self.index_buffer.add_index(2)
        self.index_buffer.add_index(1)
        self.index_buffer.add_index(3)
        