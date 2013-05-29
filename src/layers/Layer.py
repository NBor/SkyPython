'''
Created on 2013-05-28

@author: Neil
'''

class Layer(object):
    '''
    classdocs
    '''
    
    def register_with_renderer(self, rend_controller):
        self.render_map.clear()
        self.render_controller = rend_controller
        self.update_layer_for_controller_change()
        
    def set_visible(self, visible_bool):
        raise NotImplementedError("not done")

    def add_update_closure(self, closure):
        if self.render_controller != None:
            self.render_controller.add_update_closure(closure)
    
    def remove_update_callback(self, closure):
        if self.render_controller != None:
            self.render_controller.remove_update_callback(closure)
            
    def redraw(self):
        raise NotImplementedError("not done yet")
    
    def set_sources(self):
        raise NotImplementedError("not done yet")
    
    def create_render_manager(self):
        raise NotImplementedError("not done yet")
    
    def get_preference_id(self):
        return "source_provider." + self.layerNameId()
    
    def get_layer_name(self):
        raise NotImplementedError("need strings.xml")

    def __init__(self):
        '''
        Constructor
        '''
        self.render_map = {}
        self.render_controller = None