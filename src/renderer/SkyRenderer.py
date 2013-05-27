'''
Created on 2013-05-26

@author: Neil
'''

import math
from PointObjectManager import PointObjectManager
from RenderState import RenderState
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
    
        #gl.glClear(GL10.GL_COLOR_BUFFER_BIT);
    
        for managers in self.layers_to_managers.values():
            for manager in managers:
                manager.draw(None)
        #checkForErrors(gl);
        
        # Queue updates for the next frame.
        #for (UpdateClosure update : mUpdateClosures) {
        #  update.run();
        #}
        
    def on_surfaced_created(self):
        raise NotImplementedError("not implemented yet")
    
    def on_surface_changed(self):
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
        
        
        