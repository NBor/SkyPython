'''
Created on 2013-05-28

@author: Neil
'''

from utils.Enumeration import enum
from utils.Runnable import Runnable

class RenderManager(object):
    '''
    classdocs
    '''
    
    def queue_enabled(self, enable_bool, controller):
        def run_method():
            self.manager.enable(enable_bool)
        
        msg = "Enabling" if enable_bool else "Disabling" + " manager " + str(self.manager)
        controller.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_max_field_of_view(self, fov, controller):
        def run_method():
            self.manager.max_radius_of_view = fov
        
        msg = "Setting manager max field of view: " + str(fov)
        controller.queueRunnable(msg, command_type.DATA, Runnable(run_method))
        
    def queue_objects(self, sources, update_type, controller):
        def run_method():
            self.manager.update_objects(sources, update_type)
        
        msg = "Setting source objects"
        controller.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def __init__(self, mgr):
        '''
        constructor
        '''
        # Render Object Manager
        self.manager = mgr
        
command_type = enum(VIEW=0, DATA=1, SYNCHRONIZATION=3)

class RendererControllerBase(object):
    '''
    classdocs
    '''
    
    def create_point_manager(self, layer_id):
        manager = RenderManager(self.renderer.create_point_manager(layer_id))
        self.queue_add_manager(manager)
        return manager
        
    def create_line_manager(self, layer_id):
        manager = RenderManager(self.renderer.create_line_manager(layer_id))
        self.queue_add_manager(manager)
        return manager
    
    def create_label_manager(self, layer_id):
        manager = RenderManager(self.renderer.create_label_manager(layer_id))
        self.queue_add_manager(manager)
        return manager
    
    def create_image_manager(self, layer_id):
        manager = RenderManager(self.renderer.create_image_manager(layer_id))
        self.queue_add_manager(manager)
        return manager

    def queue_night_vision_mode(self, enable_bool):
        def run_method():
            self.renderer.render_state.night_vision_mode = enable_bool
        
        msg = "Setting night vision mode: " + str(enable_bool)
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_field_of_view(self, fov):
        def run_method():
            self.renderer.set_radius_of_view(fov)
        
        msg = "Setting fov: " + str(fov)
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_text_angle(self, angle_in_radians):
        def run_method():
            self.renderer.set_text_angle(angle_in_radians)
            
        msg = "Setting text angle: " + str(angle_in_radians)
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_viewer_up_direction(self, gc_up):
        def run_method():
            self.renderer.set_viewer_up_direction(gc_up)
        
        msg = "Setting up direction: " + str(gc_up)
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_set_view_orientation(self, dirX, dirY, dirZ, upX, upY, upZ):
        def run_method():
            self.renderer.set_view_orientation(dirX, dirY, dirZ, upX, upY, upZ)
        
        msg = "Setting view orientation"
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_enable_sky_gradient(self, sun_pos):
        def run_method():
            self.renderer.enable_sky_gradient(sun_pos)
        
        msg = "Enabling sky gradient at: " + str(sun_pos)
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_disable_sky_gradient(self):
        def run_method():
            self.renderer.disable_sky_gradient()
        
        msg = "Disabling sky gradient"
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def queue_enable_search_overlay(self):
        raise NotImplementedError("not done this class")
    
    def queue_disable_search_overlay(self):
        raise NotImplementedError("not done this class")
    
    def add_update_closure(self, closure):
        def run_method():
            self.renderer.add_update_closure(closure)
        
        msg = "Setting update callback"
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def remove_update_callback(self, closure):
        raise NotImplementedError("not done this class")

    def queue_add_manager(self, render_manager):
        def run_method():
            self.renderer.add_object_manager(render_manager.manager)
        
        msg = "Adding manager: " + str(render_manager)
        self.queue_runnable(msg, command_type.DATA, Runnable(run_method))
    
    def wait_until_finished(self):
        raise NotImplementedError("not done this class")
    
    def queue_runnable(self, msg, cmd_type, runnable, q=None):
        if q == None:
            q = self.queuer
        q.put(runnable)

    def __init__(self, skyrenderer):
        '''
        Constructor
        '''
        self.renderer = skyrenderer