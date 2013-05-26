'''
Created on 2013-05-14

@author: Neil
'''

from layers.LayerManager import LayerManager
from layers.NewStarsLayer import NewStarsLayer
from control.AstronomerModel import AstronomerModel
from control.ZeroMagneticDeclinationCalculator import ZeroMagneticDeclinationCalculator as ZMDC

def instantiate_layer_manager(layer_manager):
    '''
    Need to implement all the other layers
    '''
    if layer_manager == None:
        layer_manager = LayerManager()
        layer_manager.add_layer(NewStarsLayer())
        return layer_manager
    else:
        return layer_manager

def start_application():
    layer_manager = instantiate_layer_manager(None)
    model = AstronomerModel(ZMDC())
    
    # based on this models current view display stars in that region

if __name__ == '__main__':
    start_application()