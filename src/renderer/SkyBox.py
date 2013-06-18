'''
Created on 2013-06-17

@author: Neil
'''

import math
from RendererObjectManager import RendererObjectManager
from rendererUtil.VertexBuffer import VertexBuffer
from rendererUtil.ColorBuffer import ColorBuffer
from rendererUtil.IndexBuffer import IndexBuffer
from units.Vector3 import Vector3
from units.GeocentricCoordinates import GeocentricCoordinates
from utils.VectorUtil import cross_product, normalized

class SkyBox(RendererObjectManager):
    '''
    classdocs
    '''
    NUM_VERTEX_BANDS = 8
    # This number MUST be even
    NUM_STEPS_IN_BAND = 10
    
    # Used to make sure rounding error doesn't make us have off-by-one errors in our iterations.
    EPSILON = 1e-3
    
    def reload(self, gl, full_reload):
        self.vertex_buffer.reload()
        self.color_buffer.reload()
        self.index_buffer.reload()
        
    def set_sun_position(self, new_pos):
        self.sun_pos = new_pos.copy()
        
    def draw_internal(self, gl):
        if self.render_state.night_vision_mode:
            return
    
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)
        gl.glDisableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glFrontFace(gl.GL_CW)
        gl.glCullFace(gl.GL_BACK)
        
        gl.glShadeModel(gl.GL_SMOOTH)
        
        gl.glPushMatrix()
    
        # Rotate the sky box to the position of the sun.
        cp = cross_product(Vector3(0, 1, 0), self.sun_pos)
        cp = normalized(cp)
        angle = 180.0 / math.pi * math.acos(self.sun_pos.y)
        gl.glRotatef(angle, cp.x, cp.y, cp.z)
        
        self.vertex_buffer.set(gl)
        self.color_buffer.set(gl)
        
        self.index_buffer.draw(gl, gl.GL_TRIANGLES)
        
        gl.glPopMatrix()

    def __init__(self, layer_id, texture_manager):
        '''
        Constructor
        '''
        RendererObjectManager.__init__(self, layer_id, texture_manager)
        
        self.vertex_buffer = VertexBuffer(0, True)
        self.color_buffer = ColorBuffer(0, True)
        self.index_buffer = IndexBuffer(0, True)
        self.sun_pos = GeocentricCoordinates(0, 1, 0)
        
        num_vertices = self.NUM_VERTEX_BANDS * self.NUM_STEPS_IN_BAND
        num_indices = (self.NUM_VERTEX_BANDS-1) * self.NUM_STEPS_IN_BAND * 6
        self.vertex_buffer.reset(num_vertices)
        self.color_buffer.reset(num_vertices)
        self.index_buffer.reset(num_indices)
        
        sin_angles = [0.0] * self.NUM_STEPS_IN_BAND
        cos_angles = [0.0] * self.NUM_STEPS_IN_BAND
        
        angle_in_band = 0
        d_angle = 2* math.pi / float(self.NUM_STEPS_IN_BAND - 1)
        for i in range(0, self.NUM_STEPS_IN_BAND):
            sin_angles[i] = math.sin(angle_in_band)
            cos_angles[i] = math.cos(angle_in_band)
            angle_in_band += d_angle
            
        band_step = 2.0 / float((self.NUM_VERTEX_BANDS-1) + self.EPSILON)
        
        vb = self.vertex_buffer
        cb = self.color_buffer
        band_pos = 1
        for band in range(0, self.NUM_VERTEX_BANDS):
            a, r, g, b = 0, 0, 0, 0
            
            if band_pos > 0:
                intensity = long(band_pos * 20 + 50) & 0xFFFFFFFF
                a = 0xFF
                r = (intensity << 16) & 0x00FF0000
                g = (intensity << 16) & 0x0000FF00
                b = (intensity << 16) & 0x000000FF
            else:
                intensity = long(band_pos * 40 + 40) & 0xFFFFFFFF
                color = (intensity << 16) | (intensity << 8) | (intensity)
                a = 0xFF
                r = color & 0x00FF0000
                g = color & 0x0000FF00
                b = color & 0x000000FF
            
            band_pos -= band_step
        
            sin_phi = math.sqrt(1 - band_pos*band_pos) if band_pos > -1 else 0
            for i in range(0, self.NUM_STEPS_IN_BAND):
                vb.add_point(Vector3(cos_angles[i] * sin_phi, band_pos, sin_angles[i] * sin_phi))
                cb.add_color(a, r, g, b)
        
        ib = self.index_buffer
        
        # Set the indices for the first band.
        top_band_start = 0
        bottom_band_start = self.NUM_STEPS_IN_BAND
        for triangle_band in range(0, self.NUM_VERTEX_BANDS-1):
            for offset_from_start in range(0, self.NUM_STEPS_IN_BAND-1):
                # Draw one quad as two triangles.
                top_left = (top_band_start + offset_from_start)
                top_right = (top_left + 1)
                
                bottom_left = (bottom_band_start + offset_from_start)
                bottom_right = (bottom_left + 1)
                
                # First triangle
                ib.add_index(top_left)
                ib.add_index(bottom_right)
                ib.add_index(bottom_left)
                
                # Second triangle
                ib.add_index(top_right)
                ib.add_index(bottom_right)
                ib.add_index(top_left)
                
            # Last quad: connect the end with the beginning.
                
            # Top left, bottom right, bottom left
            ib.add_index((top_band_start + self.NUM_STEPS_IN_BAND - 1))
            ib.add_index(bottom_band_start)
            ib.add_index((bottom_band_start + self.NUM_STEPS_IN_BAND - 1))
            
            # Top right, bottom right, top left
            ib.add_index(top_band_start)
            ib.add_index(bottom_band_start)
            ib.add_index((top_band_start + self.NUM_STEPS_IN_BAND - 1))
            
            
            top_band_start += self.NUM_STEPS_IN_BAND
            bottom_band_start += self.NUM_STEPS_IN_BAND
            
            