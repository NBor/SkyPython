'''
Created on 2013-05-28

@author: Neil
'''

from utils.Enumeration import enum

class RenderManager(object):
    '''
    classdocs
    '''
    # Render Object Manager
    manager = None
    
    def queue_enabled(self):
        raise NotImplementedError("not done")
    
    def queue_max_field_of_view(self):
        raise NotImplementedError("not done")
    
    def __init__(self, mgr):
        '''
        constructor
        '''
        self.manager = mgr
        
class PointManager(RenderManager):
    '''
    classdocs
    '''
    
    def queue_objects(self):
        raise NotImplementedError("not done")
    
    def __init__(self, point_object_manager):
        '''
        constructor
        '''
        RenderManager.__init__(self, point_object_manager)
        
class LineManager(RenderManager):
    '''
    classdocs
    '''
    
    def queue_objects(self):
        raise NotImplementedError("not done")
    
    def __init__(self, line_object_manager):
        '''
        constructor
        '''
        RenderManager.__init__(self, line_object_manager)
        
class LabelManager(RenderManager):
    '''
    classdocs
    '''
    
    def queue_objects(self):
        raise NotImplementedError("not done")
    
    def __init__(self, label_object_manager):
        '''
        constructor
        '''
        RenderManager.__init__(self, label_object_manager)
        
class ImageManager(RenderManager):
    '''
    classdocs
    '''
    
    def queue_objects(self):
        raise NotImplementedError("not done")
    
    def __init__(self, image_object_manager):
        '''
        constructor
        '''
        RenderManager.__init__(self, image_object_manager)
        
############################################################################
command_type = enum(VIEW=0, DATA=1, SYNCHRONIZATION=3)

class RendererControllerBase(object):
    '''
    classdocs
    '''
    renderer = None
    
    def create_point_manager(self, layer_id):
        manager = PointManager(self.renderer.create_point_manager(layer_id))
        #queueAddManager(manager);
        return manager
        
    def create_line_manager(self, layer_id):
        raise NotImplementedError("no manager")
    
    def create_label_manager(self, layer_id):
        raise NotImplementedError("no manager")
    
    def create_image_manager(self, layer_id):
        raise NotImplementedError("no manager")

    def queue_night_vision_mode(self):
        raise NotImplementedError("not done this class")
    
    def queue_field_of_view(self):
        raise NotImplementedError("not done this class")
    
    def queue_text_angle(self):
        raise NotImplementedError("not done this class")
    
    def queue_viewer_up_direction(self):
        raise NotImplementedError("not done this class")
    
    def queue_set_view_orientation(self):
        raise NotImplementedError("not done this class")
    
    def queue_enable_sky_gradient(self):
        raise NotImplementedError("not done this class")
    
    def queue_diable_sky_gradient(self):
        raise NotImplementedError("not done this class")
    
    def queue_enable_search_overlay(self):
        raise NotImplementedError("not done this class")
    
    def queue_disable_search_overlay(self):
        raise NotImplementedError("not done this class")
    
    def add_update_closure(self, closure):
        raise NotImplementedError("not done this class")
    
    def remove_update_callback(self, closure):
        raise NotImplementedError("not done this class")

    def queue_add_manager(self):
        ############################################################################ Important to finish this
        raise NotImplementedError("not done this class")
    
    def wait_until_finished(self):
        raise NotImplementedError("not done this class")
    
    def queue_runnable(self):
        raise NotImplementedError("not done this class")

    def __init__(self, skyrenderer):
        '''
        Constructor
        '''
        self.renderer = skyrenderer
        