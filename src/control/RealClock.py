'''
Created on 2013-06-19

@author: Neil
'''

import time

class RealClock(object):
    '''
    classdocs
    '''
    def get_time(self):
        return time.time()

    def __init__(self):
        '''
        Constructor
        '''
        