'''
Created on 2013-05-29

@author: Neil
'''

from FileBasedLayer import FileBasedLayer

class NewConstellationsLayer(FileBasedLayer):
    '''
    classdocs
    '''
    def get_layer_id(self):
        return -101
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.1"

    def __init__(self):
        '''
        Constructor
        '''
        FileBasedLayer.__init__(self, "assets/constellations.binary")

if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    