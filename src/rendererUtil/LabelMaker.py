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
Created on 2013-06-10

@author: Neil Borle
'''

import math
import numpy as np
from PySide.QtGui import QBitmap, QColor, QFont, QImage, QFontMetrics, QPainter
from PySide.QtOpenGL import QGLWidget

class LabelMaker(object):
    '''
    Creates a texture and paints text on top of it. This is then rendered
    within an appropriately coloured rectangle.
    '''
    class LabelData(object):
        '''
        A class which contains data that describes a label and 
        its position in the texture.
        '''
        def set_texture_data(self, width_pixels, height_pixels, 
                                    crop_u, crop_v, crop_w, crop_h,
                                    texel_width, texel_height):
            self.width_in_pixels = width_pixels
            self.height_in_pixels = height_pixels
            
            text_coords_list = [0.0]*8
            # lower left
            text_coords_list[0] = crop_u * texel_width
            text_coords_list[1] = crop_v * texel_height
            
            # upper left
            text_coords_list[2] = crop_u * texel_width
            text_coords_list[3] = (crop_v + crop_h) * texel_height
            
            # lower right
            text_coords_list[4] = (crop_u + crop_w) * texel_width
            text_coords_list[5] = crop_v * texel_height
            
            # upper right
            text_coords_list[6] = (crop_u + crop_w) * texel_width
            text_coords_list[7] = (crop_v + crop_h) * texel_height
            
            self.text_coords = np.array(text_coords_list, dtype=np.float32)
      
            self.crop = [crop_u, crop_v, crop_w, crop_h]
            
        
        def __init__(self, m_string='', m_color=0xFFFFFFFF, m_font_size=24):
            '''
            constructor
            '''
            self.string = m_string
            self.color = m_color
            self.font_size = m_font_size
            
            self.width_in_pixels = 0
            self.height_in_pixels = 0
            self.text_coords = None
            self.crop = None
            
    def initialize(self, gl, render_state, labels, texture_manager):
        '''
        Call to initialize the class. Call whenever the surface has been created.
        '''
        self.texture = texture_manager.create_texture(gl)
        self.texture.bind(gl)
        
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, 
                           gl.GL_NEAREST)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, 
                           gl.GL_NEAREST)
    
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, 
                           gl.GL_CLAMP_TO_EDGE)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, 
                           gl.GL_CLAMP_TO_EDGE)
    
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, gl.GL_REPLACE)
        
        min_height = self.add_labels_internal(gl, render_state, False, labels)
    
        # Round up to the nearest power of two, since textures have to be a power of two in size.
        rounded_height = 1
        while rounded_height < min_height:
            rounded_height <<= 1
            
        self.strike_height = rounded_height;
        
        self.texel_width = (1.0 / float(self.strike_width))
        self.texel_height = (1.0 / float(self.strike_height))
        
        self.begin_adding(gl)
        self.add_labels_internal(gl, render_state, True, labels)
        self.end_adding(gl)
        
        return self.texture

    def shutdown(self, gl):
        '''
        Call when the surface has been destroyed
        '''
        if self.texture == None:
            self.texture.delete(gl)

    def add_labels_internal(self, gl, render_state, draw_to_canvas, labels):
        '''
        call to add a list of labels
        '''
        text_paint = QPainter()
        
        if draw_to_canvas:
            text_paint.begin(self.bitmap)
            text_paint.setRenderHints(QPainter.Antialiasing)
        
        u = 0
        v = 0
        line_height = 0

        for label in labels:
            ascent = 0
            descent = 0
            measured_text_width = 0
            
            height = 0
            width = 0


            font_size = label.font_size
            while True:
                metrics = None
                
                if draw_to_canvas:
                    mask = 0x000000FF
                    b = (label.color >> 16) & mask 
                    g = (label.color >> 8) & mask
                    r = label.color & mask
                    ######################################################################## LINE CHANGED
                    text_paint.setPen(QColor(0, 0, 0))
                    #text_paint.setPen(QColor(r, g, b))
                    
                    # The value 0.75 is hard coded representing phone pixel density
                    text_paint.setFont(QFont('Veranda', font_size * 0.75))
                    
                    # Paint.ascent is negative, so negate it.
                    metrics = text_paint.fontMetrics()
                else:
                    # The value 0.75 is hard coded representing phone pixel density
                    metrics = QFontMetrics(QFont('Veranda', font_size * 0.75))
                ascent = math.ceil(metrics.ascent())
                descent = math.ceil(metrics.descent())
                measured_text_width = math.ceil(metrics.boundingRect(label.string).width())
                
                height = int(ascent) + int(descent)
                width = int(measured_text_width)
                
                # If it's wider than the screen, try it again with a font size of 1
                # smaller.
                font_size -= 1
                if font_size < 0 or width < render_state.screen_width:
                    break
                
            next_u = 0
            
            # Is there room for this string on the current line?
            if u + width > self.strike_width:
                # No room, go to the next line:
                u = 0
                next_u = width
                v += line_height
                line_height = 0
            else:
                next_u = u + width

            line_height = max(line_height, height)
            if (v + line_height > self.strike_height) and draw_to_canvas:
                raise Exception("out of texture space.")

            v_base = v + ascent
            
            if draw_to_canvas:
                text_paint.drawText(int(u), int(v_base), label.string)
                
                label.set_texture_data(width, height, u, v + height, width, -height, 
                                       self.texel_width, self.texel_height)
            u = next_u
        
        if draw_to_canvas:
            text_paint.end()
            
        return v + line_height

    def begin_adding(self, gl):
        #Bitmap.Config config = mFullColor ? Bitmap.Config.ARGB_4444 : Bitmap.Config.ALPHA_8
        #mBitmap = Bitmap.createBitmap(mStrikeWidth, mStrikeHeight, config)
        self.bitmap = QBitmap(self.strike_width, self.strike_height)
        self.bitmap.clear()

    def end_adding(self, gl):
        self.texture.bind(gl)
        
        '''
        IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT
        The image has to be mirrored for some reason
        '''
        img = QImage(self.bitmap.toImage()).mirrored()
        img = QGLWidget.convertToGLFormat(img)
        
        gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width(), img.height(), 0, gl.GL_RGBA, 
                        gl.GL_UNSIGNED_BYTE, str(img.bits()))
        
        # This particular bitmap is no longer needed
        self.bitmap = None


    def __init__(self, color_bool):
        '''
        Constructor
        '''
        self.strike_height = -1
        self.strike_width = 512
        self.full_color = color_bool
        self.bitmap = None
        self.texture = None
        self.texel_height = None # convert texel to V
        self.texel_width = None  # convert texel to U

if __name__ == "__main__":
    import OpenGL.GL as gl
    LM = LabelMaker(True)
    LM.begin_adding(gl)