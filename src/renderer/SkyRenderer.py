'''
Created on 2013-05-26

@author: Neil
'''
from OpenGL import GL
import math
from RenderState import RenderState
from PointObjectManager import PointObjectManager
from rendererUtil.GLBuffer import GLBuffer
from rendererUtil.SkyRegionMap import SkyRegionMap

class SkyRenderer(object):
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
    
    sky_box = None
    overlayManager = None

    render_state = RenderState()
    
    projection_matrix = None
    view_matrix = None

    # Indicates whether the transformation matrix has changed since the last
    # time we started rendering
    must_update_view = True
    must_update_projection = True
    
    update_closures = {}
    update_listener = None #Need to finish this
    
    all_managers = []
    texture_manager = None
    managers_to_reload = []
    layers_to_managers = {}
    
    def on_draw_frame(self, gl):
        # Initialize any of the unloaded managers.
        for m_reload_data in self.managers_to_reload:
            m_reload_data.manager.reload(gl, m_reload_data.full_reload)
        
        self.managers_to_reload = []
    
        #maybeUpdateMatrices(gl);
    
        # Determine which sky regions should be rendered.
        self.render_state.active_sky_region_set = \
            SkyRegionMap().get_active_regions(
                self.render_state.look_dir,
                self.render_state.radius_of_view,
                self.render_state.screen_width / float(self.render_state.screen_height))
    
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
    
        for managers in self.layers_to_managers.values():
            for manager in managers:
                manager.draw(gl)
        #checkForErrors(gl);
        
        # Queue updates for the next frame.
        #for (UpdateClosure update : mUpdateClosures) {
        #  update.run();
        #}
        
    def on_surfaced_created(self, gl):
        gl.glEnable(gl.GL_DITHER);

        # Some one-time OpenGL initialization can be made here
        # probably based on features of this particular context
        gl.glHint(gl.GL_PERSPECTIVE_CORRECTION_HINT,
                  gl.GL_FASTEST)
        
        gl.glClearColor(0, 0, 0, 0)
        gl.glEnable(gl.GL_CULL_FACE)
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glDisable(gl.GL_DEPTH_TEST)
        
        # Release references to all of the old textures.
        #mTextureManager.reset()
        
        extensions = GL.glGetString(GL.GL_EXTENSIONS)
        
        # Determine if the phone supports VBOs or not, and set this on the GLBuffer.
        # TODO(jpowell): There are two extension strings which seem applicable.
        # There is GL_OES_vertex_buffer_object and GL_ARB_vertex_buffer_object.
        # I can't find any documentation which explains the difference between
        # these two.  Most phones which support one seem to support both,
        # except for the Nexus One, which only supports ARB but doesn't seem
        # to benefit from using VBOs anyway.  I should figure out what the
        # difference is and use ARB too, if I can.
        can_use_vbo = False
        if "GL_OES_vertex_buffer_object" in extensions:
            can_use_vbo = True
            
            # VBO support on the Cliq and Behold is broken and say they can
            # use them when they can't.  Explicitly disable it for these devices.
            bad_models = ["MB200", "MB220", "Behold" ]
            #for (String model : bad_models) {
            #    if (android.os.Build.MODEL.contains(model)) {
            #        can_use_vbo = false;
            #    }
            #}
            setattr(GLBuffer, "can_use_VBO", can_use_vbo)
            
            # Reload all of the managers.
            for rom in self.all_managers:
                rom.reload(gl, True)
    
    def on_surface_changed(self, gl):
        raise NotImplementedError("not implemented yet")
    
    def set_radius_of_view(self, deg):
        self.render_state.radius_of_view = deg
        self.must_update_projection = True
        
    def add_update_closure(self, update):
        raise NotImplementedError("not implemented yet")
    
    def remove_update_callback(self, update):
        raise NotImplementedError("not implemented yet")
    
    def set_view_updirection(self, gc_up):
        raise NotImplementedError("Overlay manager not implemented yet")
    
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
        index = self.all_managers.index(m)
        self.all_managers.pop(index)
        
        index = self.layers_to_managers[m.layer].index(m)
        self.layers_to_managers[m.layer].pop(index)
    
    def enable_sky_gradient(self):
        raise NotImplementedError("not implemented yet")
    
    def disable_sky_gradient(self):
        raise NotImplementedError("not implemented yet")
    
    def enable_search_overlay(self, gc_target, target_name):
        raise NotImplementedError("not implemented yet")
    
    def disable_search_overlay(self):
        raise NotImplementedError("not implemented yet")
    
    def set_night_vision_mode(self):
        raise NotImplementedError("not implemented yet")
    
    def set_text_angle(self, rad):
        TWO_OVER_PI = 2.0 / math.pi
        PI_OVER_TWO = math.pi / 2.0

        new_angle = round(rad * TWO_OVER_PI) * PI_OVER_TWO

        self.render_state.up_angle = new_angle
        
    def set_view_orientation(self, dir_x, dir_y, dir_z,
                             up_x, up_y, up_z):
        raise NotImplementedError("not implemented yet")
    
    def get_width(self):
        return self.render_state.screen_width
    
    def get_height(self):
        return self.render_state.screen_height

    def check_for_errors(self):
        raise NotImplementedError("not implemented yet")
    
    def update_view(self, gl):
        raise NotImplementedError("not implemented yet")
    
    def update_perspective(self, gl):
        raise NotImplementedError("not implemented yet")
    
    def maybe_update_matrices(self, gl):
        raise NotImplementedError("not implemented yet")
    
    def create_point_manager(self, new_layer):
        return PointObjectManager(new_layer, self.texture_manager)
    
    def create_poly_line_manager(self):
        raise NotImplementedError("not implemented yet")
    
    def create_label_manager(self):
        raise NotImplementedError("not implemented yet")
    
    def create_image_manager(self):
        raise NotImplementedError("not implemented yet")

    def __init__(self):
        '''
        Constructor
        '''
        #mTextureManager = new TextureManager(res);
    
        # The skybox should go behind everything.
        #mSkyBox = new SkyBox(Integer.MIN_VALUE, mTextureManager);
        #mSkyBox.enable(false);
        #addObjectManager(mSkyBox);
    
        #The overlays go on top of everything.
        #mOverlayManager = new OverlayManager(Integer.MAX_VALUE, mTextureManager);
        #addObjectManager(mOverlayManager);
        
        
        