'''
Created on 2013-05-26

@author: Neil
'''

import threading
from src.utils.Enumeration import enum

class RendererObjectManager(object):
    '''
    ABSTRACT CLASS DO NOT DIRECTLY INSTANTIATE
    '''
    lock = threading.RLock()
    max_radius_of_view = 360   # in degrees
    # Used to distinguish between different renderers, so we can have sets of them.
    s_index = 0

    update_type = enum(Reset=0, UpdatePositions=1, UpdateImages=2)
    
    def compare_to(self, render_object_manager):
        raise NotImplementedError("Not implemented")
    
    def draw(self, gl):
        if self.enabled and self.render_state.radius_of_view <= self.max_radius_of_view:
            self.draw_internal(gl)
            
    def queue_for_reload(self, bool_full_reload):
        self.listener(self, bool_full_reload)

    def __init__(self, new_layer, new_texture_manager):
        '''
        Constructor
        '''
        self.layer = new_layer
        self.texture_manager = new_texture_manager
        self.enabled = True
        self.render_state = None
        self.listener = None
        with self.lock:
            self.index = self.s_index + 1