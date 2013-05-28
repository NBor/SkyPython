'''
Created on 2013-05-14

@author: Neil
'''

from layers.LayerManager import LayerManager
from layers.NewStarsLayer import NewStarsLayer
from source.AstronomicalSource import AstronomicalSource
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
    
    points = []    
    for proto_source in layer_manager.layers[0].astro_sources:
        new_astro = AstronomicalSource()
        new_astro.names = proto_source.names
        new_astro.geocentric_coords = proto_source.get_geo_coords()
        new_astro.image_sources = proto_source.get_images()
        new_astro.point_sources = proto_source.get_points()
        new_astro.line_sources = proto_source.get_lines()
        new_astro.text_sources = proto_source.get_labels()
        points += new_astro.point_sources
    POM.update_objects(points, None)
    
    sky_renderer = SkyRenderer()
    sky_renderer.add_object_manager(POM)

    sky_renderer.on_draw_frame(None)

if __name__ == '__main__':
    start_application()