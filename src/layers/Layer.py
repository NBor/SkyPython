'''
Created on 2013-05-28

@author: Neil
'''

import threading

from ..source.PointSource import PointSource
from ..source.LineSource import LineSource
from ..source.TextSource import TextSource
from ..source.ImageSource import ImageSource

class Layer(object):
    '''
    classdocs
    '''
    reentrant_lock = threading.RLock()
    
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
            
    def redraw(self, points, lines, texts, images, update_type):
        if self.render_controller == None:
            return
        
        self.reentrant_lock.acquire()
        try:
            atomic = self.render_controller.create_atomic()
            self.set_sources(points, update_type, PointSource, atomic)
            self.set_sources(lines, update_type, LineSource, atomic)
            self.set_sources(texts, update_type, TextSource, atomic)
            self.set_sources(images, update_type, ImageSource, atomic)
            self.render_controller.queue_atomic(atomic)
        finally:
            self.reentrant_lock.release()
    
    def set_sources(self, sources, update_type, clazz, atomic):       
        if sources == None: 
            return
        
        manager = None
        if clazz not in self.render_map.keys():
            manager = self.create_render_manager(clazz, atomic)
            self.render_map[clazz] = manager
        else:
            manager = self.render_map[clazz]
            
        manager.queue_objects(sources, update_type, atomic)
    
    def create_render_manager(self, clazz, controller):
        if clazz is PointSource:
            return controller.create_point_manager(self.get_layer_id())
        elif clazz is LineSource:
            return controller.create_line_manager(self.get_layer_id())
        elif clazz is TextSource:
            return controller.create_label_manager(self.get_layer_id())
        elif clazz is ImageSource:
            return controller.create_image_manager(self.get_layer_id())
        else:
            raise Exception("class is of unknown type")
    
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