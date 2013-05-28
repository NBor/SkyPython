'''
Created on 2013-05-22

@author: Neil
'''

from search.SearchResult import SearchResult

class SourceLayer(object):
    '''
    classdocs
    '''
    text_sources = []
    image_sources = []
    point_sources = []
    line_sources = []
    astro_sources = []
    
    # prefix_store = prefixstore class
    search_index = {}
    should_update = False
    
    def init(self):
        self.astro_sources = []
        self.initialize_astro_sources(self.astro_sources)
        
        for source in self.astro_sources:
            self.image_sources += source.get_images()
            self.line_sources += source.get_lines()
            self.point_sources += source.get_points()
            self.text_sources += source.get_labels()
            
            if source.names != []:
                gc_search_loaction = source.get_geo_coords()
                for name in source.names:
                    self.search_index[str(name).lower()] = \
                        SearchResult(name, gc_search_loaction)
                    # prefix_store.add(str(name).lower())
    
    def __init__(self, boolean):
        '''
        Constructor
        '''
        self.should_update = boolean
        