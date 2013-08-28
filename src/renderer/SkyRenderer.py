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


Created on 2013-05-26

@author: Neil Borle
'''

import math
import numpy as np
from OpenGL import GL
from PySide.QtOpenGL import QGLWidget
from RenderState import RenderState
from SkyBox import SkyBox
from OverlayManager import OverlayManager
from PointObjectManager import PointObjectManager
from PolyLineObjectManager import PolyLineObjectManager
from LabelObjectManager import LabelObjectManager
from ImageObjectManager import ImageObjectManager
from src.rendererUtil.TextureManager import TextureManager
from src.rendererUtil.GLBuffer import GLBuffer
from src.rendererUtil.SkyRegionMap import SkyRegionMap
from src.units.GeocentricCoordinates import GeocentricCoordinates
from src.utils import Matrix4x4
from src.utils.VectorUtil import cross_product
from src.utils.DebugOptions import Debug

class SkyRenderer(QGLWidget):
    '''
    Main class that handles all of the rendering
    '''
    class ManagerReloadData(object):
        '''
        encapsulates what is needed to reload a manager
        '''
        def __init__(self, mgr, reload_bool):
            self.manager = mgr
            self.full_reload = reload_bool

    # Indicates whether the transformation matrix has changed since the last
    # time we started rendering
    must_update_view = True
    must_update_projection = True
    
    def paintGL(self):
        # Initialize any of the unloaded managers.
        for m_reload_data in self.managers_to_reload:
            m_reload_data.manager.reload(GL, m_reload_data.full_reload)
        
        self.managers_to_reload = []
    
        self.maybe_update_matrices(GL)
    
        # Determine which sky regions should be rendered.
        self.render_state.active_sky_region_set = \
            SkyRegionMap().get_active_regions(
                self.render_state.look_dir,
                self.render_state.radius_of_view,
                self.render_state.screen_width / float(self.render_state.screen_height))
    
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)
        
        for managers in self.layers_to_managers.values():
            # reverse to render images, text, lines then points
            for manager in managers[::-1]:
                manager.draw(GL)
        self.check_for_errors(GL)
        
        # Queue updates for the next frame.
        for update in self.update_closures:
            update.run()
        
    def initializeGL(self):
        GL.glEnable(GL.GL_DITHER);

        # Some one-time OpenGL initialization can be made here
        # probably based on features of this particular context
        GL.glHint(GL.GL_PERSPECTIVE_CORRECTION_HINT,
                  GL.GL_FASTEST)
        
        GL.glClearColor(0, 0, 0, 0)
        GL.glEnable(GL.GL_CULL_FACE)
        GL.glShadeModel(GL.GL_SMOOTH)
        GL.glDisable(GL.GL_DEPTH_TEST)
        
        # Release references to all of the old textures.
        self.texture_manager.reset()
        
        extensions = GL.glGetString(GL.GL_EXTENSIONS)
        
        # Determine if the phone supports VBOs or not, and set this on the GLBuffer.
        can_use_vbo = False
        if "GL_OES_vertex_buffer_object" in extensions: # this will never pass at the moment
            can_use_vbo = True
            
            # VBO support on the Cliq and Behold is broken and say they can
            # use them when they can't.  Explicitly disable it for these devices.
            #bad_models = ["MB200", "MB220", "Behold" ]
            #for (String model : bad_models) {
            #    if (android.os.Build.MODEL.contains(model)) {
            #        can_use_vbo = false;
            #    }
            #}
            setattr(GLBuffer, "can_use_VBO", can_use_vbo)
            
            # Reload all of the managers.
            for rom in self.all_managers:
                rom.reload(GL, True)
    
    def resizeGL(self, width, height):
        
        self.render_state.set_screen_size(width, height)
        self.overlay_manager.resize(GL, width, height)

        # Need to set the matrices.
        self.must_update_view = True
        self.must_update_projection = True

        GL.glViewport(0, 0, width, height)
    
    def set_radius_of_view(self, deg):
        self.render_state.radius_of_view = deg
        self.must_update_projection = True
        
    def add_update_closure(self, update):
        self.update_closures.append(update)
    
    def remove_update_callback(self, update):
        if update in self.update_closures:
            i = self.update_closures.index(update)
            self.update_closures.pop(i)
    
    def set_viewer_up_direction(self, gc_up):
        self.overlay_manager.set_view_up_direction(gc_up)
    
    def add_object_manager(self, m):
        m.render_state = self.render_state
        m.listener = self.update_listener
        self.all_managers.append(m)
        self.managers_to_reload.append(self.ManagerReloadData(m, True))
        
        if m.layer in self.layers_to_managers.keys():
            self.layers_to_managers[m.layer].append(m)
        else:
            self.layers_to_managers[m.layer] = [m]
            
    def remove_object_manager(self, m):
        if m in self.all_managers:
            index = self.all_managers.index(m)
            self.all_managers.pop(index)
        
        if m.layer in self.layers_to_managers.keys() and \
                m in self.layers_to_managers[m.layer]:
            index = self.layers_to_managers[m.layer].index(m)
            self.layers_to_managers[m.layer].pop(index)
    
    def enable_sky_gradient(self, sun_position):
        self.sky_box.set_sun_position(sun_position)
        self.sky_box.enabled = True
    
    def disable_sky_gradient(self):
        self.sky_box.enabled = False
    
    def enable_search_overlay(self, gc_target, target_name):
        raise NotImplementedError("not implemented yet")
    
    def disable_search_overlay(self):
        raise NotImplementedError("not implemented yet")
    
    def set_night_vision_mode(self, enabled_bool):
        self.render_state.night_vision_mode = enabled_bool
    
    def set_text_angle(self, rad):
        TWO_OVER_PI = 2.0 / math.pi
        PI_OVER_TWO = math.pi / 2.0

        new_angle = round(rad * TWO_OVER_PI) * PI_OVER_TWO

        self.render_state.up_angle = new_angle
        
    def set_view_orientation(self, dir_x, dir_y, dir_z,
                             up_x, up_y, up_z):
        # Normalize the look direction
        dir_len = math.sqrt(dir_x*dir_x + dir_y*dir_y + dir_z*dir_z)
        one_over_dir_len = 1.0 / float(dir_len)
        dir_x *= one_over_dir_len
        dir_y *= one_over_dir_len
        dir_z *= one_over_dir_len
        
        # We need up to be perpendicular to the look direction, so we subtract
        # off the projection of the look direction onto the up vector
        look_dot_up = dir_x * up_x + dir_y * up_y + dir_z * up_z
        up_x -= look_dot_up * dir_x
        up_y -= look_dot_up * dir_y
        up_z -= look_dot_up * dir_z
        
        # Normalize the up vector
        up_len = math.sqrt(up_x*up_x + up_y*up_y + up_z*up_z)
        one_over_up_len = 1.0 / float(up_len)
        up_x *= one_over_up_len
        up_y *= one_over_up_len
        up_z *= one_over_up_len
        
        self.render_state.set_look_dir(GeocentricCoordinates(dir_x, dir_y, dir_z))
        self.render_state.set_up_dir(GeocentricCoordinates(up_x, up_y, up_z))
        
        self.must_update_view = True
        
        self.overlay_manager.set_view_orientation(GeocentricCoordinates(dir_x, dir_y, dir_z), 
                                                  GeocentricCoordinates(up_x, up_y, up_z))
        
    def get_width(self):
        return self.render_state.screen_width
    
    def get_height(self):
        return self.render_state.screen_height

    def check_for_errors(self, gl):
        error = gl.glGetError()
        if error != 0:
            raise RuntimeError("GL error: " + str(error))
    
    def update_view(self, gl):
        # Get a vector perpendicular to both, pointing to the right, by taking
        # lookDir cross up.
        look_dir = self.render_state.look_dir.copy()
        up_dir = self.render_state.up_dir.copy()
        right = cross_product(look_dir, up_dir)
        
        if self.DEBUG_MODE != None:
            from src.units.Vector3 import Vector3
            look_dir = Vector3(Debug.LOOKDIRVECTORS[self.DEBUG_MODE][0], 
                               Debug.LOOKDIRVECTORS[self.DEBUG_MODE][1], 
                               Debug.LOOKDIRVECTORS[self.DEBUG_MODE][2])
            up_dir = Vector3(Debug.UPDIRVECTORS[self.DEBUG_MODE][0], 
                             Debug.UPDIRVECTORS[self.DEBUG_MODE][1], 
                             Debug.UPDIRVECTORS[self.DEBUG_MODE][2])
            right = Vector3(Debug.RIGHTVECTORS[self.DEBUG_MODE][0], 
                            Debug.RIGHTVECTORS[self.DEBUG_MODE][1], 
                            Debug.RIGHTVECTORS[self.DEBUG_MODE][2])
        
        self.view_matrix = Matrix4x4.create_view(look_dir, up_dir, right)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
        adjust_matrix = Matrix4x4.Matrix4x4([0.0, 0.0, -1.0, 0.0,
                                             0.0, 1.0, -0.0, 0.0,
                                             1.0, 0.0, -0.0, 0.0,
                                             0.0, 0.0, 0.0, 1.0])
        matrix = Matrix4x4.multiply_MM(self.view_matrix, adjust_matrix)
        
        # Invert the left/right rotation of the matrix
        matrix.values[2] *= -1
        matrix.values[8] *= -1
        
        # Invert these so that we don't rotate in and out of the unit sphere
        matrix.values[1] *= -1
        matrix.values[4] *= -1
        
        matrix = np.array(matrix.values, dtype=np.float32)
        #matrix = np.array(self.view_matrix.values, dtype=np.float32)
        gl.glLoadMatrixf(matrix)
    
    def update_perspective(self, gl):
        
        if self.DEBUG_MODE != None:
            self.render_state.radius_of_view = Debug.RADIUSOFVIEW
        
        self.projection_matrix = Matrix4x4.create_perspective_projection(
                self.get_width(),
                self.get_height(),
                self.render_state.radius_of_view * 3.141593 / 360.0)
        
        gl.glMatrixMode(gl.GL_PROJECTION)
            
        matrix = np.array(self.projection_matrix.values, dtype=np.float32)
        gl.glLoadMatrixf(matrix)
        
        # The image is mirrored so scale it to make the polygon fronts into backs 
        gl.glScalef(-1.0, 1.0, 1.0)
        
        # Switch back to the model view matrix.
        gl.glMatrixMode(gl.GL_MODELVIEW)
    
    def maybe_update_matrices(self, gl):
        update_transform = self.must_update_view or self.must_update_projection
        if self.must_update_view:
            self.update_view(gl)
            self.must_update_view = False
        if self.must_update_projection:
            self.update_perspective(gl)
            self.must_update_projection = False
            
        if update_transform:
            # Device coordinates are a square from (-1, -1) to (1, 1).  Screen
            # coordinates are (0, 0) to (width, height).  Both coordinates
            # are useful in different circumstances, so we'll pre-compute
            # matrices to do the transformations from world coordinates
            # into each of these.
            transform_to_device = Matrix4x4.multiply_MM(self.projection_matrix, self.view_matrix)
            
            translate = Matrix4x4.create_translation(1.0, 1.0, 0.0)
            scale = Matrix4x4.create_scaling(self.render_state.screen_width * 0.5, 
                                             self.render_state.screen_height * 0.5, 1)
            
            transform_to_screen = \
            Matrix4x4.multiply_MM(Matrix4x4.multiply_MM(scale, translate), transform_to_device)
            
            self.render_state.set_tranformation_matrices(transform_to_device, transform_to_screen)
    
    def create_point_manager(self, new_layer):
        return PointObjectManager(new_layer, self.texture_manager)
    
    def create_line_manager(self, new_layer):
        return PolyLineObjectManager(new_layer, self.texture_manager)
    
    def create_label_manager(self, new_layer):
        return LabelObjectManager(self, new_layer, self.texture_manager)
    
    def create_image_manager(self, new_layer):
        return ImageObjectManager(new_layer, self.texture_manager)

    def __init__(self, debug_mode=None):
        '''
        Constructor
        '''
        QGLWidget.__init__(self)
        
        self.DEBUG_MODE = debug_mode
        
        self.texture_manager = TextureManager()
        self.render_state = RenderState()
        
        self.projection_matrix = None
        self.view_matrix = None
        
        self.update_closures = []

        self.all_managers = []
        self.managers_to_reload = []
        self.layers_to_managers = {}
        
        def queue_for_reload(rom, full_reload):
            self.managers_to_reload.append(self.ManagerReloadData(rom, full_reload))
        
        self.update_listener = queue_for_reload
    
        # The skybox should go behind everything.
        self.sky_box = SkyBox(0x10000000, self.texture_manager)
        self.sky_box.enabled = False
        self.add_object_manager(self.sky_box)
    
        #The overlays go on top of everything.
        self.overlay_manager = OverlayManager(0xEFFFFFFF, self.texture_manager)
        self.add_object_manager(self.overlay_manager)
        
        