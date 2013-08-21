'''
Created on 2013-06-19

@author: Neil
'''

import time

class RealClock(object):
    '''
    A real clock that provides the current
    time since the epoch
    '''
    def get_time(self):
        return time.time()

    def __init__(self):
        '''
        Constructor
        '''
        