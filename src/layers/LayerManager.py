'''
Created on 2013-05-24

@author: Neil
'''

from NewStarsLayer import NewStarsLayer
from NewConstellationsLayer import NewConstellationsLayer
from NewMessierLayer import NewMessierLayer
from GridLayer import GridLayer
from EclipticLayer import EclipticLayer
from HorizonLayer import HorizonLayer
from MeteorShowerLayer import MeteorShowerLayer
from SkyGradientLayer import SkyGradientLayer

def instantiate_layer_manager(model):
    '''
    Need to implement all the other layers
    '''
    layer_manager = LayerManager()
    layer_manager.add_layer(NewStarsLayer())
    layer_manager.add_layer(NewConstellationsLayer())
    layer_manager.add_layer(NewMessierLayer())
    #planets layer
    layer_manager.add_layer(GridLayer(24, 19))
    layer_manager.add_layer(EclipticLayer())
    layer_manager.add_layer(HorizonLayer(model))
    layer_manager.add_layer(MeteorShowerLayer(model))
    layer_manager.add_layer(SkyGradientLayer(model))
    layer_manager.init_layers()
    return layer_manager

class LayerManager(object):
    '''
    classdocs
    '''

    def add_layer(self, layer):
        self.layers.append(layer)
        
    def init_layers(self):
        for layer in self.layers:
            layer.initialize()
            
    def register_with_renderer(self, renderer_controller):
        for layer in self.layers:
            layer.register_with_renderer(renderer_controller)
            #prefId = layer.getPreferenceId()
            #visible_bool = sharedPreferences.getBoolean(prefId, true)
            #layer.set_visible(visible_bool)
    
    def on_shared_preference_change(self):
        raise NotImplementedError("not implemented")
    
    def get_string(self):
        return "Layer Manager"
    
    def search_by_object_name(self):
        raise NotImplementedError("not implemented")
    
    def get_object_names_matching_prefix(self):
        raise NotImplementedError("not implemented")
    
    def is_layer_visible(self):
        raise NotImplementedError("not implemented")

    def __init__(self):
        '''
        Constructor
        '''
        self.layers = []