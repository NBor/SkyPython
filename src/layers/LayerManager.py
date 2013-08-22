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
// Original Author: Not stated
// 
// Notification of Change: The original java source code has been heavily
// modified in that it has been rewritten in the python programming
// language and additionaly may component and ideas not found in the 
// original source code.
'''

'''
Created on 2013-05-24

@author: Neil Borle
'''

from NewStarsLayer import NewStarsLayer
from NewConstellationsLayer import NewConstellationsLayer
from NewMessierLayer import NewMessierLayer
from PlanetsLayer import PlanetsLayer
from GridLayer import GridLayer
from EclipticLayer import EclipticLayer
from HorizonLayer import HorizonLayer
from MeteorShowerLayer import MeteorShowerLayer
from SkyGradientLayer import SkyGradientLayer
from src.utils.DebugOptions import Debug

def instantiate_layer_manager(model, shared_prefs):
    '''
    Add a new instance of each layer and initialize it
    '''
    layer_manager = LayerManager(shared_prefs)
    layer_manager.add_layer(NewStarsLayer())
    layer_manager.add_layer(NewConstellationsLayer())
    layer_manager.add_layer(NewMessierLayer())
    layer_manager.add_layer(PlanetsLayer(model))
    layer_manager.add_layer(GridLayer(24, 19))
    layer_manager.add_layer(EclipticLayer())
    layer_manager.add_layer(HorizonLayer(model))
    layer_manager.add_layer(MeteorShowerLayer(model))
    layer_manager.add_layer(SkyGradientLayer(model))
    
    if Debug.LAYER == "STARS ONLY":
        layer_manager = LayerManager()
        layer_manager.add_layer(NewStarsLayer())
    elif Debug.LAYER == "FIRST 3":
        layer_manager = LayerManager()
        layer_manager.add_layer(NewStarsLayer())
        layer_manager.add_layer(NewConstellationsLayer())
        layer_manager.add_layer(NewMessierLayer())
    
    layer_manager.init_layers()
    return layer_manager

class LayerManager(object):
    '''
    Class responsible for grouping together all layers
    so that they can be controlled together.
    '''

    def add_layer(self, layer):
        self.layers.append(layer)
        
    def init_layers(self):
        for layer in self.layers:
            layer.initialize()
            
    def register_with_renderer(self, renderer_controller):
        for layer in self.layers:
            layer.register_with_renderer(renderer_controller)
            pref_id = layer.get_preference_id()
            visible_bool = self.shared_prefs.PREFERENCES[pref_id]
            layer.set_visible(visible_bool)
    
    def on_shared_preference_change(self, prefs, pref_id):
        for layer in self.layers:
            if layer.get_preference_id() == pref_id:
                visible_bool = prefs.PREFERENCES[pref_id]
                layer.set_visible(visible_bool)
    
    def get_string(self):
        return "Layer Manager"
    
    def search_by_object_name(self):
        raise NotImplementedError("not implemented")
    
    def get_object_names_matching_prefix(self):
        raise NotImplementedError("not implemented")
    
    def is_layer_visible(self, layer):
        return self.shared_prefs.PREFERENCES[layer]

    def __init__(self, shared_prefs):
        '''
        Constructor
        '''
        self.shared_prefs = shared_prefs
        self.layers = []