'''
Created on 2013-05-23

@author: Neil
'''

class Controller(object):
    '''
    Super class that forces all controller sub classes
    to have models and an enabled boolean.
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.model = None
        self.enabled = True
        
if __name__ == "__main__":
    '''
    Do nothing
    '''