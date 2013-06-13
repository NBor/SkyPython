'''
Created on 2013-06-10

@author: Neil
'''

from RendererObjectManager import RendererObjectManager

class ImageObjectManager(RendererObjectManager):
    '''
    classdocs
    '''
    def update_objects(self, image_sources, update_type):
        print "Image manager not implemented yet"
        
    def reload(self, gl, full_reload):
        pass
    
    def draw_internal(self, gl):
        pass 

    def __init__(self, new_layer, new_texture_manager):
        '''
        Constructor
        '''
        RendererObjectManager.__init__(self, new_layer, new_texture_manager)
        