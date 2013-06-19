'''
Created on 2013-05-26

@author: Neil
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
from rendererUtil.TextureManager import TextureManager
from rendererUtil.GLBuffer import GLBuffer
from rendererUtil.SkyRegionMap import SkyRegionMap
from units.GeocentricCoordinates import GeocentricCoordinates
from utils import Matrix4x4
from utils.VectorUtil import cross_product

class SkyRenderer(QGLWidget):
    '''
    classdocs
    '''
    class ManagerReloadData(object):
        '''
        classdocs
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
            for manager in managers:
                manager.draw(GL)
        #checkForErrors(GL);
        
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

    def check_for_errors(self):
        raise NotImplementedError("not implemented yet")
    
    def update_view(self, gl):
        # Get a vector perpendicular to both, pointing to the right, by taking
        # lookDir cross up.
        look_dir = self.render_state.look_dir.copy()
        up_dir = self.render_state.up_dir.copy()
        right = cross_product(look_dir, up_dir)
        
        self.view_matrix = Matrix4x4.create_view(look_dir, up_dir, right)
        
        gl.glMatrixMode(gl.GL_MODELVIEW)
#         self.view_matrix.values = [0.0, 0.0, -1.0, 0.0,
#                                    0.0, 1.0, -0.0, 0.0,
#                                    1.0, 0.0, -0.0, 0.0,
#                                    0.0, 0.0, 0.0, 1.0]
#         self.view_matrix.values = [0.0, 0.0, -1.0, 0.0,
#                                    0.0, 1.0, -0.0, 0.0,
#                                    1.0, 0.0, -0.0, 0.0,
#                                    0.0, 0.0, 0.0, 1.0]
        matrix = np.array(self.view_matrix.values, dtype=np.float32)
        gl.glLoadMatrixf(matrix)
        gl.glLoadIdentity()
    
    def update_perspective(self, gl):
        self.projection_matrix = Matrix4x4.create_perspective_projection(
                self.get_width(),
                self.get_height(),
                self.render_state.radius_of_view * 3.141593 / 360.0)
        
        gl.glMatrixMode(gl.GL_PROJECTION)
#         self.projection_matrix.values = [4.023689, 0.0, 0.0, 0.0,
#                                          0.0, 2.4142134, 0.0, 0.0,
#                                          0.0, 0.0, -1.0000019, -1.0,
#                                          0.0, 0.0, -0.02000002, 0.0]
        self.projection_matrix.values = [4.023689, 0.0, 0.0, 0.0,
                                         0.0, 2.4142134, 0.0, 0.0,
                                         0.0, 0.0, -1.0000019, -0.02000002,
                                         0.0, 0.0, 1.0, 1.0]
        matrix = np.array(self.projection_matrix.values, dtype=np.float32)
        gl.glLoadMatrixf(matrix)
        #gl.glLoadIdentity()
        
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

    def __init__(self):
        '''
        Constructor
        '''
        QGLWidget.__init__(self)
        self.texture_manager = TextureManager()
        self.render_state = RenderState()
        
        self.projection_matrix = None
        self.view_matrix = None
        
        self.update_closures = []
        self.update_listener = None #Need to finish this
        
        self.all_managers = []
        self.managers_to_reload = []
        self.layers_to_managers = {}
    
        # The skybox should go behind everything.
        self.sky_box = SkyBox(0x10000000, self.texture_manager)
        self.sky_box.enabled = False
        self.add_object_manager(self.sky_box)
    
        #The overlays go on top of everything.
        self.overlay_manager = OverlayManager(0xEFFFFFFF, self.texture_manager)
        self.add_object_manager(self.overlay_manager)
        
        
        