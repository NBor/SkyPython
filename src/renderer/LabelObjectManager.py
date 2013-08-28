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

import math
import numpy as np
from src.units.Vector3 import Vector3
from src.utils.Matrix4x4 import transform_vector
from RendererObjectManager import RendererObjectManager
from src.rendererUtil.SkyRegionMap import SkyRegionMap
from src.rendererUtil.LabelMaker import LabelMaker
from src.units.GeocentricCoordinates import GeocentricCoordinates
from src.utils.Matrix4x4 import create_rotation, multiply_MV
from src.utils.DebugOptions import Debug

class LabelObjectManager(RendererObjectManager):
    '''
    Manages the rendering of text labels by loading
    text sources into buffers for rendering and maintaining 
    these buffers.
    '''
    class label(LabelMaker.LabelData):
        '''
        A private class which extends the LabelMaker's label data with an xyz position and rgba color values.
        For the red-eye mode, it's easier to set the color in the texture to white and set the color when we render
        the label than to have two textures, one with red labels and one without. 
        '''
        
        def __init__(self, text_source):
            '''
            constructor
            '''
            LabelMaker.LabelData.__init__(self, text_source.label, 
                                          0xFFFFFFFF, text_source.font_size)
            
            if text_source.label == None or text_source.label == '':
                raise Exception("Bad label " + str(self))
            
            self.x = text_source.geocentric_coords.x
            self.y = text_source.geocentric_coords.y
            self.z = text_source.geocentric_coords.z
            
            self.offset = text_source.offset
            
            # The distance this should be rendered underneath the specified position, in world coordinates.
            self.rgb = text_source.color
            self.a = 0xFF
            self.b = (self.rgb >> 16) & 0xFF
            self.g = (self.rgb >> 8) & 0xFF
            self.r = self.rgb & 0xFF
            # fixed point values
            #self.fixed_a = int(65536.0 * self.a / 255.0) & 0xFFFFFFFF
            #self.fixed_b = int(65536.0 * self.b / 255.0) & 0xFFFFFFFF
            #self.fixed_g = int(65536.0 * self.g / 255.0) & 0xFFFFFFFF
            #self.fixed_r = int(65536.0 * self.r / 255.0) & 0xFFFFFFFF
        
    # Should we compute the regions for the labels?
    # If false, we just put them in the catchall region.
    COMPUTE_REGIONS = True
    
    def update_objects(self, labels, update_type):
        if self.update_type.Reset in update_type:
            self.labels = [None] * len(labels)
            for i in range(0, len(labels)):
                self.labels[i] = self.label(labels[i])
            self.queue_for_reload(False)
        elif self.update_type.UpdatePositions in update_type:
            if len(labels) != len(self.labels):
                return
                
            # Since we don't store the positions in any GPU memory, and do the
            # transformations manually, we can just update the positions stored
            # on the label objects.
            for i in range(0, len(self.labels)):
                pos = labels[i].gc_coords
                self.labels[i].x = pos.x
                self.labels[i].y = pos.y
                self.labels[i].z = pos.z
                

        self.sky_region_map.clear()
        for l in self.labels:
            if self.COMPUTE_REGIONS:
                region = self.sky_region_map.get_object_region(GeocentricCoordinates(l.x, l.y, l.z))
            else:
                region = self.sky_region_map.CATCHALL_REGION_ID
            self.sky_region_map.get_region_data(region).append(l)
    
    def reload(self, gl, full_reload):
        # We need to regenerate the texture.  If we're re-creating the surface 
        # (fullReload=true), all resources were automatically released by OpenGL,
        # so we don't want to try to release it again.  Otherwise, we need to
        # release it to avoid a resource leak (shutdown takes
        # care of freeing the texture).
        if not full_reload and self.label_maker == None:
            self.label_maker.shutdown(gl)
        
        self.label_maker = LabelMaker(True)
        self.texture_ref = self.label_maker.initialize(gl, self.render_state,
                                                       self.labels, self.texture_manager)
    
    def draw_internal(self, gl):
        if Debug.DRAWING == "POINTS ONLY" or Debug.DRAWING == "POINTS AND LINES": return
        
        gl.glTexEnvf(gl.GL_TEXTURE_ENV, gl.GL_TEXTURE_ENV_MODE, 
                     gl.GL_MODULATE)
    
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glActiveTexture(gl.GL_TEXTURE0)
        self.texture_ref.bind(gl)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_S,
                           gl.GL_REPEAT)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_WRAP_T,
                           gl.GL_REPEAT)
    
        self.begin_drawing(gl)
        
        # Draw the labels for the active sky regions.
        active_regions = self.render_state.active_sky_region_set
        all_active_labels = self.sky_region_map.get_data_for_active_regions(active_regions)
        
        for labels_in_region in all_active_labels:
            for l in labels_in_region:
                self.draw_label(gl, l)
                
        self.end_drawing(gl)

    
    def draw_label(self, gl, label):
        look_dir = self.render_state.look_dir
        if look_dir.x * label.x + look_dir.y * label.y + \
                look_dir.z * label.z < self.dot_product_threshold:
            return
    
        # Offset the label to be underneath the given position (so a label will 
        # always appear underneath a star no matter how the phone is rotated) 
        v = Vector3(label.x - self.label_offset.x * label.offset,
                    label.y - self.label_offset.y * label.offset,
                    label.z - self.label_offset.z * label.offset)
        
        screen_pos = transform_vector(self.render_state.transform_to_screen, v)
        
        # We want this to align consistently with the pixels on the screen, so we
        # snap to the nearest x/y coordinate, and add a magic offset of less than
        # half a pixel.  Without this, rounding error can cause the bottom and
        # top of a label to be one pixel off, which results in a noticeable
        # distortion in the text.
        MAGIC_OFFSET = 0.25
        screen_pos.x = int(screen_pos.x) + MAGIC_OFFSET
        screen_pos.y = int(screen_pos.y) + MAGIC_OFFSET
        
        gl.glPushMatrix()
        
        gl.glTranslatef(screen_pos.x, screen_pos.y, 0)
        gl.glRotatef((180.0 / math.pi) * self.render_state.up_angle, 0, 0, -1)
        gl.glScalef(label.width_in_pixels, label.height_in_pixels, 1)
        
        gl.glVertexPointer(2, gl.GL_FLOAT, 0, self.quad_buffer)
        gl.glTexCoordPointer(2, gl.GL_FLOAT, 0, label.text_coords)
        if self.render_state.night_vision_mode:
            gl.glColor4ub(0xFF, 0, 0, label.a)
        else:
            gl.glColor4ub(label.r, label.g, label.b, 128)
            
        gl.glDrawArrays(gl.GL_TRIANGLE_STRIP, 0, 4)
        
        gl.glPopMatrix()
        
    def begin_drawing(self, gl):
        '''
        Sets OpenGL state for rapid drawing
        '''
        self.texture_ref.bind(gl)
        gl.glShadeModel(gl.GL_FLAT)
        
        ########################################################################## added Blending
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
        
        gl.glEnable(gl.GL_ALPHA_TEST)
        gl.glAlphaFunc(gl.GL_GREATER, 0.5)
        gl.glEnable(gl.GL_TEXTURE_2D)
        
        # We're going to do the transformation on the CPU, so set the matrices 
        # to the identity
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPushMatrix()
        gl.glLoadIdentity()
        gl.glOrtho(0, self.render_state.screen_width,
                    0, self.render_state.screen_height,
                    -1, 1)
        
        # equivalent of a call to GLBuffer.unbind(gl)
        gl.glBindBuffer(gl.GL_ARRAY_BUFFER, 0)
        gl.glBindBuffer(gl.GL_ELEMENT_ARRAY_BUFFER, 0)
        
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_TEXTURE_COORD_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)
    
        rs = self.render_state
        
        view_width = rs.screen_width
        view_height = rs.screen_height
        
        rotation = create_rotation(rs.up_angle, rs.look_dir)
        self.label_offset = multiply_MV(rotation, rs.up_dir)
    
        # If a label isn't within the field of view angle from the target vector, it can't
        # be on the screen.  Compute the cosine of this angle so we can quickly identify these.
        DEGREES_TO_RADIANS = math.pi / 180.0
        self.dot_product_threshold = math.cos(rs.radius_of_view * DEGREES_TO_RADIANS * \
                                            (1 + view_width / float(view_height)) * 0.5)

    
    def end_drawing(self, gl):
        ##########################################################################added blending
        gl.glDisable(gl.GL_BLEND)
        
        gl.glDisable(gl.GL_ALPHA_TEST)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
        gl.glDisable(gl.GL_TEXTURE_2D)
        
        gl.glColor4f(1, 1, 1, 1)

    def __init__(self, sky_renderer, new_layer, new_texture_manager):
        '''
        Constructor
        '''
        RendererObjectManager.__init__(self, new_layer, new_texture_manager)
        
        self.label_maker = None
        self.labels = []
        self.sky_region_map = SkyRegionMap() 
  
        # These are intermediate variables set in beginDrawing() and used in
        # draw() to make the transformations more efficient
        self.label_offset = Vector3(0, 0, 0)
        self.dot_product_threshold = None
  
        self.texture_ref = None
        
        # A quad with size 1 on each size, so we just need to multiply
        # by the label's width and height to get it to the right size for each
        # label.
        vertices = [-0.5, -0.5,   # lower left
                    -0.5,  0.5,   # upper left
                    0.5, -0.5,    # lower right
                    0.5,  0.5]    # upper right
        # make the vertices fixed point? byte buffer?
        self.quad_buffer = np.array(vertices, dtype=np.float32)     
        # We want to initialize the labels of a sky region to an empty list.
        def construct_method():
            return []
        
        self.sky_region_map.region_data_factory = \
            SkyRegionMap.RegionDataFactory(construct_method)
            
            