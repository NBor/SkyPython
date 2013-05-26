'''
Created on 2013-05-25

@author: Neil
'''

from rendererUtil.SkyRegionMap import SkyRegionMap

class PointObjectManager(object):
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

    def __init__(self, layer=None, texture_manager=None):
        '''
        Constructor
        '''
        # super.__init__() and change inputs to not be default
        self.sky_regions.region_data_factory = self.RegionDataFactory()
        