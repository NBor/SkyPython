'''
Created on 2013-05-28

@author: Neil
'''

class SearchResult(object):
    '''
    classdocs
    '''
    gc_coord = None
    capitalized_name = None

    def __init__(self, name, coord):
        '''
        Constructor
        '''
        self.gc_coord = coord
        self.capitalized_name = name