'''
Created on 2013-05-22

@author: Neil
'''

from units.GeocentricCoordinates import GeocentricCoordinates as GC

class Pointing(object):
    '''
    This class is to be ONLY used with AstronomerModel.
    This class holds state on the user direction of view
    '''
    gc_line_of_sight = None
    gc_perpendicular = None

    def get_line_of_sight(self):
        return self.gc_line_of_sight.copy()
        
    def get_perpendicular(self):
        return self.gc_perpendicular.copy()

    #Only the AstronomerModel should change this.
    def update_perpendicular(self, new_perpendicular):
        self.perpendicular.assign(new_perpendicular)
 
    #Only the AstronomerModel should change this.
    def update_line_of_sight(self, new_line_of_sight):
        self.gc_line_of_sight.assign(new_line_of_sight)

    def __init__(self, line_of_sight=GC(1, 0, 1), perp=GC(0, 1, 0)):
        '''
        Constructor
        '''
        self.gc_line_of_sight = line_of_sight.copy()
        self.gc_perpendicular = perp.copy()
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for debugging
    '''
    