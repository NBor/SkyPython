'''
Created on 2013-05-25

@author: Neil
'''

from RendererObjectManager import RendererObjectManager
from rendererUtil.SkyRegionMap import SkyRegionMap

class PointObjectManager(RendererObjectManager):
    '''
    classdocs
    '''

    class RegionData(object):
        '''
        classdocs
        '''
        sources = []
        vertex_buffer = []
        color_buffer = []
        text_coord_buffer = []
        index_buffer = []
    
        def __init__(self):
            '''
            constructor
            '''
       
    class RegionDataFactory(object):
        '''
        classdocs
        '''
        def construct(self):
            return PointObjectManager.RegionData()
        
        def __init__(self):
            '''
            constructor
            '''
            
    NUM_STARS_IN_TEXTURE = 2
    MINIMUM_NUM_POINTS_FOR_REGIONS = 200
    COMPUTE_REGIONS = True
    sky_regions = SkyRegionMap()
    texture_ref = None
    
    def update_objects(self):
        raise NotImplemented("should do this soon")
    
    def reload(self, gl, bool_full_reload):
        raise NotImplementedError("need OpenGL support")
    
    def draw_internal(self, gl):
        raise NotImplementedError("need OpenGL support")

    def __init__(self, new_layer=None, new_texture_manager=None):
        '''
        change inputs to not be default
        '''
        RendererObjectManager.__init__(self, new_layer, new_texture_manager)
        self.sky_regions.region_data_factory = self.RegionDataFactory()
        