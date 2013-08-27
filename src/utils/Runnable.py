'''
Created on 2013-06-07

@author: Neil Borle
'''

class Runnable(object):
    '''
    A Runnable class with a run method so that actions
    can be queued and then run uniformly. This substitutes
    for java's runnable interface.
    '''
    def run(self):
        raise Exception("This method must be overwritten")

    def __init__(self, run_method):
        '''
        Constructor
        '''
        self.run = run_method
        
if __name__ == "__main__":
    
    def run_method():
        print "Hello world"
    
    r = Runnable(run_method)
    r.run()