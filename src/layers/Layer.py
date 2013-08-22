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
// Original Author: John Taylor, Brent Bryan
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-28

@author: Neil Borle
'''

import threading

from src.source.PointSource import PointSource
from src.source.LineSource import LineSource
from src.source.TextSource import TextSource
from src.source.ImageSource import ImageSource

class Layer(object):
    '''
    Base class for any layer (is a combination of layer.java
    and AbstractLayer.java in the original code).
    '''
    reentrant_lock = threading.RLock()
    
    def register_with_renderer(self, rend_controller):
        self.render_map.clear()
        self.render_controller = rend_controller
        self.update_layer_for_controller_change()
        
    def set_visible(self, visible_bool):
        '''
        Makes this layer visible or invisible based on user
        selection with the preference buttons.
        '''
        with self.reentrant_lock:
            atomic = self.render_controller.create_atomic()
            for render_manager in self.render_map.values():
                render_manager.queue_enabled(visible_bool, atomic)
            self.render_controller.queue_atomic(atomic)

    def add_update_closure(self, closure):
        if self.render_controller != None:
            self.render_controller.add_update_closure(closure)
    
    def remove_update_callback(self, closure):
        if self.render_controller != None:
            self.render_controller.remove_update_callback(closure)
            
    def redraw(self, points, lines, texts, images, update_type):
        '''
        Forces a redraw of the layer by removing all object managers.
        Updates the renderer (using the given UpdateType), with then given set 
        of UI elements.  Depending on the value of UpdateType, current sources 
        will either have their state updated, or will be overwritten by the 
        given set of UI elements.
        '''
        if self.render_controller == None:
            return
        
        with self.reentrant_lock:
            atomic = self.render_controller.create_atomic()
            self.set_sources(points, update_type, PointSource, atomic)
            self.set_sources(lines, update_type, LineSource, atomic)
            self.set_sources(texts, update_type, TextSource, atomic)
            self.set_sources(images, update_type, ImageSource, atomic)
            self.render_controller.queue_atomic(atomic)
    
    def set_sources(self, sources, update_type, clazz, atomic):
        '''
        Given an input source (point/line/text/image) a corresponding
        object manager is created and stored in the render_map dictionary.
        ''' 
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