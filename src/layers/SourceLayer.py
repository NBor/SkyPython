'''
Created on 2013-05-22

@author: Neil
'''

from Layer import Layer
from renderer.RendererObjectManager import RendererObjectManager
from search.SearchResult import SearchResult

class SourceLayer(Layer):
    '''
    classdocs
    '''
    class SourceUpdateClosure(object):
        '''
        classdocs
        '''
        source_layer = None
        
        def run(self):
            self.source_layer.refresh_sources()
        
        def __init__(self, layer):
            '''
            constructor
            '''
            self.source_layer = layer
    
    search_index = {}
    # prefix_store = prefixstore class
    should_update = False
    closure = None
    
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
        #self.update_layer_for_controller_change()
        
    def update_layer_for_controller_change(self):
        self.refresh_sources(False)
        if self.should_update:
            if self.closure == None:
                self.closure = self.SourceUpdateClosure(self)
            self.add_update_closure()
            
    def refresh_sources(self, update_types=set()): # this needs to be synchronized!
        #for astro_source in self.astro_sources:
        #    update_types = set(update_types + astro_source.update())

        if len(update_types) != 0:
            self.redraw(update_types)
    
    def redraw(self, update_types=set()):
        if len(update_types) == 0:
            r = RendererObjectManager(0, None)
            self.refresh_sources(set([r.update_type.Reset]))
        else:
            Layer.redraw(self, self.point_sources, self.line_sources, \
                         self.text_sources, self.image_sources, update_types)
            
    def search_by_object_name(self):
        raise NotImplementedError("haven't done searching yet")
    
    def get_object_names_matching_prefix(self):
        raise NotImplementedError("haven't done searching yet")
    
    def __init__(self, boolean):
        '''
        Constructor
        '''
        self.should_update = boolean
        self.text_sources = []
        self.image_sources = []
        self.point_sources = []
        self.line_sources = []
        self.astro_sources = []