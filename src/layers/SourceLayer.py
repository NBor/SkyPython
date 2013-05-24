'''
Created on 2013-05-22

@author: Neil
'''

class SourceLayer(object):
    '''
    classdocs
    '''
    text_sources = []
    image_sources = []
    point_sources = []
    line_sources = []
    astro_sources = []
    
    search_index = {}
    should_update = False
    
    def init(self):
        self.astro_sources = []
        for source in self.astro_sources:
            self.image_sources += source.image_sources
            self.line_sources += source.line_sources
            self.point_sources += source.point_sources
            self.text_sources += source.text_sources
            
            if source.names != []:
                geo = source.get_geo_coords()
                '''
                NOT FINISHED THIS
                '''
    
    def __init__(self, boolean):
        '''
        Constructor
        '''
        self.should_update = boolean
        