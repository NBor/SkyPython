'''
Created on 2013-05-29

@author: Neil
'''

from FileBasedLayer import FileBasedLayer

class NewMessierLayer(FileBasedLayer):
    '''
    Displays messier objects in the renderer
    '''
    
    def get_layer_id(self):
        return -102
    
    def get_layer_name_id(self):
        raise NotImplementedError("not implemented yet")
    
    def get_preference_id(self):
        return "source_provider.2"

    def __init__(self):
        '''
        Constructor
        '''
        FileBasedLayer.__init__(self, "assets/messier.binary")

if __name__ == "__main__":
    '''
    Do nothing
    '''
    