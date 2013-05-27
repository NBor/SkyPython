'''
Created on 2013-05-14

@author: Neil
'''

from layers.LayerManager import LayerManager
from layers.NewStarsLayer import NewStarsLayer
from control.AstronomerModel import AstronomerModel
from renderer.PointObjectManager import PointObjectManager
from renderer.SkyRenderer import SkyRenderer
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
    layer_manager.init_layers()
    model = AstronomerModel(ZMDC())
    POM = PointObjectManager(-100, None)
    
    layer_manager.layers[0].init_astro_sources()
    points = []
    for source in layer_manager.layers[0].astro_sources:
        points += source.point_sources
    POM.update_objects(points, None)
    
    sky_renderer = SkyRenderer()
    sky_renderer.add_object_manager(POM)

    sky_renderer.on_draw_frame(None)

if __name__ == '__main__':
    start_application()