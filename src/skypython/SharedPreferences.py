'''
Created on 2013-08-12

@author: Neil Borle
'''

class SharedPreferences(object):
    '''
    classdocs
    '''
    PREFERENCES = {"source_provider.0" : True,
                   "source_provider.1" : True,
                   "source_provider.2" : True,
                   "source_provider.3" : True,
                   "source_provider.4" : True,
                   "source_provider.5" : True,
                   "source_provider.6" : True,
                   "source_provider.7" : True,
                   "source_provider.8" : True }
    ALLOW_ROTATION = False

    def __init__(self):
        '''
        Constructor
        '''
        