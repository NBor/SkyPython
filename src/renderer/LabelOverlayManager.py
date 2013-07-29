'''
Created on 2013-07-26

@author: Neil
'''

from ..rendererUtil.LabelMaker import LabelMaker
from ..rendererUtil.IndexBuffer import IndexBuffer
from ..rendererUtil.VertexBuffer import VertexBuffer

class LabelOverlayManager(object):
    '''
    classdocs
    '''
    class Label(LabelMaker.LabelData):
        '''
        classdocs
        '''
        
        def __init__(self, text, color, size):
            '''
            constructor
            '''
            LabelMaker.LabelData.__init__(self, text, color, size)
            self.enabled = True
            self.x, self.y = 0, 0
            self.alpha = 1

    def initialize(self, gl, render_state, labels, texture_manager):
        self.labels = labels[:]
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
        