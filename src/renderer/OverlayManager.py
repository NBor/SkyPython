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
// Original Author: Not stated
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


Created on 2013-06-18

@author: Neil Borle
'''

import math
from OpenGL.GLU import gluOrtho2D
from RendererObjectManager import RendererObjectManager
from src.rendererUtil.ColoredQuad import ColoredQuad
from src.units.Vector3 import Vector3
from src.utils.VectorUtil import cross_product, normalized
from src.utils.Matrix4x4 import create_identity, create_rotation, multiply_MV

class OverlayManager(RendererObjectManager):
    '''
    Manages the various overlay classes.
    '''
    must_update_transformed_orientation = True
    searching = False
    
    def reload(self, gl, full_reload):
        pass
        #mSearchArrow.reloadTextures(gl, res, textureManager());
        #mCrosshair.reloadTextures(gl, res, textureManager());
        
    def resize(self, gl, screen_width, screen_height):
        self.width = screen_width
        self.height = screen_height
        
        # If the search target is within this radius of the center of the screen, the user is
        # considered to have "found" it.
        #float searchTargetRadius = Math.min(screenWidth, screenHeight) - 20;
        #mSearchHelper.setTargetFocusRadius(searchTargetRadius);
        #mSearchHelper.resize(screenWidth, screenHeight);
    
        #mSearchArrow.resize(gl, screenWidth, screenHeight, searchTargetRadius);
        #mCrosshair.resize(gl, screenWidth, screenHeight);
        
        self.dark_quad = ColoredQuad(0, 0, 0, 0.6, 
                                     0, 0, 0, 
                                     screen_width, 0, 0, 
                                     0, screen_height, 0)
        
    def set_view_orientation(self, look_dir, up_dir):
        self.look_dir = look_dir.copy()
        self.up_dir = up_dir.copy()
        self.must_update_transformed_orientation = True
        
    def draw_internal(self, gl):
        self.update_transformed_orientation_if_necessary()
        
        self.set_up_matrices(gl)
    
        if self.searching:
            #mSearchHelper.setTransform(getRenderState().getTransformToDeviceMatrix());
            #mSearchHelper.checkState();
            
            #transitionFactor = mSearchHelper.getTransitionFactor();
            
            # Darken the background.
            self.dark_quad.draw(gl)
            
            # Draw the crosshair.
            #mCrosshair.draw(gl, mSearchHelper, getRenderState().getNightVisionMode());
            
            # Draw the search arrow.
            #mSearchArrow.draw(gl, mTransformedLookDir, mTransformedUpDir, mSearchHelper,
            #                  getRenderState().getNightVisionMode())
    
        self.restore_matrices(gl)
        
    def set_view_up_direction(self, viewer_up):
        if abs(viewer_up.y) < 0.999:
            cp = cross_product(viewer_up, Vector3(0, 0, 0))
            cp = normalized(cp)
            self.geo_to_viewer_transform = create_rotation(math.acos(viewer_up.y), cp)
        else:
            self.geo_to_viewer_transform = create_identity()
            
        self.must_update_transformed_orientation = True
        
    def enable_search_overlay(self):
        raise NotImplementedError("Not done yet")
    
    def disable_search_overlay(self):
        raise NotImplementedError("Not done yet")
    
    def set_up_matrices(self, gl):
        # Save the matrix values.
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPushMatrix()
        gl.glLoadIdentity()
    
        gl.glMatrixMode(gl.GL_MODELVIEW);
        gl.glPushMatrix()
        left = self.width / 2.0
        bottom = self.height / 2.0
        gl.glLoadIdentity()
        gluOrtho2D(left, -left, bottom, -bottom)
        
    def restore_matrices(self, gl):
        # Restore the matrices.
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glPopMatrix()
    
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glPopMatrix()
        
    def update_transformed_orientation_if_necessary(self):
        if self.must_update_transformed_orientation and self.searching:
            
            self.transformed_look_dir = \
                multiply_MV(self.geo_to_viewer_transform, self.look_dir)
                
            self.transformed_up_dir = \
                multiply_MV(self.geo_to_viewer_transform, self.up_dir)
                
            self.must_update_transformed_orientation = False

    def __init__(self, layer_id, new_texture_manager):
        '''
        Constructor
        '''
        RendererObjectManager.__init__(self, layer_id, new_texture_manager)
        self.width = 2
        self.height = 2
        self.geo_to_viewer_transform = create_identity()
        self.look_dir = Vector3(0, 0, 0)
        self.up_dir = Vector3(0, 1, 0)
        self.transformed_look_dir = Vector3(0, 0, 0)
        self.transformed_up_dir = Vector3(0, 1, 0)
        
        #search_helper = SearchHelper()
        self.dark_quad = None
        #self.search_arrow = SearchArrow()
        #crosshair = CrosshairOverlay()
        
        