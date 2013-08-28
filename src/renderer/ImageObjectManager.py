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


Created on 2013-06-10

@author: Neil Borle
'''

from PySide.QtGui import QImage
from PySide.QtOpenGL import QGLWidget
from RendererObjectManager import RendererObjectManager
from src.rendererUtil.TextureManager import TextureManager
from src.rendererUtil.VertexBuffer import VertexBuffer
from src.rendererUtil.TextCoordBuffer import TextCoordBuffer
from src.units.Vector3 import Vector3
from src.utils.DebugOptions import Debug

class ImageObjectManager(RendererObjectManager):
    '''
    Manages the rendering of image objects, specifically
    it takes in a list of image sources and fills several
    buffers so that these images can be rendered.
    '''
    class Image():
        def __init__(self):
            self.name = None
            self.pixmap = None
            self.texture_id = None
            self.use_blending = False
    
    def update_objects(self, image_sources, update_types):
        '''
        takes a list of image sources and creates new buffers
        for these sources.
        '''
        
        # hack to get rid of blank meteor showers.
        image_sources = [img for img in image_sources if not img.is_blank]
        
        if self.update_type.Reset not in update_types and \
                len(image_sources) != len(self.images):
            return
        self.updates = self.updates | update_types # set union
        
        num_vertices = len(image_sources) * 4
        vb = self.vertex_buffer
        vb.reset(num_vertices)
        
        tcb = self.text_coord_buffer
        tcb.reset(num_vertices)
        
        images = []
        reset = (self.update_type.Reset in update_types) or (self.update_type.UpdateImages in update_types)
        if reset:
            images = [None] * len(image_sources)
        else:
            images = self.images
            
        if reset:
            for i in range(0, len(image_sources)):
                ims = image_sources[i]
                
                images[i] = self.Image()
                images[i].name = "no url"
                images[i].use_blending = False
                images[i].pixmap = ims.pixmap_image
                
        # Update the positions in the position and tex coord buffers.
        if reset or self.update_type.UpdatePositions in update_types:
            for i in range(0, len(image_sources)):
                ims = image_sources[i]
                xyz = ims.geocentric_coords
                px = xyz.x
                py = xyz.y
                pz = xyz.z
                
                u = ims.get_horizontal_corner()
                ux = u[0]
                uy = u[1]
                uz = u[2]
                
                v = ims.get_verical_corner()
                vx = v[0]
                vy = v[1]
                vz = v[2]
                
                # lower left
                vb.add_point(Vector3(px - ux - vx, py - uy - vy, pz - uz - vz))
                tcb.add_text_coord(0, 1)
                
                # upper left
                vb.add_point(Vector3(px - ux + vx, py - uy + vy, pz - uz + vz))
                tcb.add_text_coord(0, 0)
                
                # lower right
                vb.add_point(Vector3(px + ux - vx, py + uy - vy, pz + uz - vz))
                tcb.add_text_coord(1, 1)
                
                # upper right
                vb.add_point(Vector3(px + ux + vx, py + uy + vy, pz + uz + vz))
                tcb.add_text_coord(1, 0)

        # We already set the image in reset, so only set them here if we're
        # not doing a reset.
        if self.update_type.UpdateImages in update_types:
            for i in range(0, len(image_sources)):
                ims = image_sources[i]
                images[i].pixmap = ims.pixmap_image
        self.images = images
        self.queue_for_reload(False)
        
    def reload(self, gl, full_reload):
        imgs = self.images
        reload_buffers = False
        reload_images = False
        
        if full_reload:
            reload_buffers =True
            reload_images = True
            # If this is a full reload, all the textures were automatically deleted,
            # so just create new arrays so we won't try to delete the old ones again.
            self.textures = [None] * len(imgs)
            self.red_textures = [None] * len(imgs)
        else:
            # Process any queued updates.
            reset = self.update_type.Reset in self.updates
            reload_buffers = reload_buffers or reset or self.update_type.UpdatePositions in self.updates
            reload_images = reload_images or reset or self.update_type.UpdateImages in self.updates
            self.updates = set()
            
        if reload_buffers:
            self.vertex_buffer.reload()
            self.text_coord_buffer.reload()
        if reload_images:
            for i in range(0, len(self.textures)):
                #If the image is already allocated, delete it.
                if self.textures[i] != None:
                    self.textures[i].delete(gl)
                    self.red_textures[i].delete(gl)
                    
                bmp = self.images[i].pixmap
                self.textures[i] = TextureManager().create_texture(gl)
                self.textures[i].bind(gl)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
                
                '''
                IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT IMPORTANT
                The image has to be mirrored for some reason
                '''
                q_img = QImage(bmp.toImage()).mirrored()
                img = QGLWidget.convertToGLFormat(q_img)
                
                gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGB, img.width(), img.height(), 0, gl.GL_RGBA, 
                                gl.GL_UNSIGNED_BYTE, str(img.bits()))
                
                
                self.red_textures[i] = TextureManager().create_texture(gl)
                self.red_textures[i].bind(gl)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S, gl.GL_CLAMP_TO_EDGE)
                gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T, gl.GL_CLAMP_TO_EDGE)
                
                red_pixels = self.create_red_image(q_img)
                red_pixels = QGLWidget.convertToGLFormat(red_pixels)
                
                gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, red_pixels.width(), red_pixels.height(), 
                                0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, str(red_pixels.bits()))
    
    def draw_internal(self, gl):
        if Debug.DRAWING == "POINTS ONLY" or Debug.DRAWING == "POINTS AND LINES": return
        
        if self.vertex_buffer.num_vertices == 0:
            return
            
        gl.glEnable(gl.GL_TEXTURE_2D)
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
        
        self.vertex_buffer.set(gl)
        self.text_coord_buffer.set(gl)
        
        textures = self.textures
        red_textures = self.red_textures
        for i in range(0, len(textures)):
            if self.images[i].use_blending:
                gl.glEnable(gl.GL_BLEND)
                gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            else:
                gl.glEnable(gl.GL_ALPHA_TEST)
                gl.glAlphaFunc(gl.GL_GREATER, 0.5)
                
            if self.render_state.night_vision_mode:
                red_textures[i].bind(gl)
            else:
                textures[i].bind(gl)
            gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 4 * i, 4)

            if self.images[i].use_blending:
                gl.glDisable(gl.GL_BLEND)
            else:
                gl.glDisable(gl.GL_ALPHA_TEST)
        
        gl.glDisable(gl.GL_TEXTURE_2D)
        
    def create_red_image(self, img):
        new_img = QImage(img)
        
        for x in range(0, img.width()):
            for y in range(0, img.height()):
                pix = img.pixel(x, y)
                r = pix & 0xFF
                g = (pix >> 8) & 0xFF
                b = (pix >> 16) & 0xFF
                alpha_mask = pix & 0xFF000000
                
                new_img.setPixel(x, y, (alpha_mask | ((r + g + b) / 3)))
                
        return new_img
        

    def __init__(self, new_layer, new_texture_manager):
        '''
        Constructor
        '''
        RendererObjectManager.__init__(self, new_layer, new_texture_manager)
        
        self.vertex_buffer = VertexBuffer()
        self.text_coord_buffer = TextCoordBuffer()
        self.images = []
        self.textures = []
        self.red_textures = []
        
        self.updates = set()
        