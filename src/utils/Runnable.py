'''
Created on 2013-06-07

@author: Neil Borle
'''

class Runnable(object):
    '''
    classdocs
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