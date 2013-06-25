'''
Created on 2013-05-16

@author: Neil
'''

from PySide.QtGui import QBitmap
from Source import Source
from units.Vector3 import Vector3
from utils.Colors import colors
from utils.VectorUtil import negate, normalized, cross_product

class ImageSource(Source):
    '''
    // These two vectors, along with Source.xyz, determine the position of the
    // image object.  The corners are as follows
    //
    //  xyz-u+v   xyz+u+v
    //     +---------+     ^
    //     |   xyz   |     | v
    //     |    .    |     .
    //     |         |
    //     +---------+
    //  xyz-u-v    xyz+u-v
    //
    //          .--->
    //            u
    '''
    image_scale = 1

    def get_horizontal_corner(self):
        return [self.ux, self.uy, self.uz]
    
    def get_verical_corner(self):
        return [self.vx, self.vy, self.vz]
    
    def set_up_vector(self, up_v):
        p = self.geocentric_coords
        u = negate(normalized(cross_product(p, up_v)));
        v = cross_product(u, p);
        v.scale(self.image_scale);
        u.scale(self.image_scale);
        
        self.ux = u.x;
        self.uy = u.y;
        self.uz = u.z;
        
        self.vx = v.x;
        self.vy = v.y;
        self.vz = v.z;
    
    def set_image_id(self, input_id):
        self.bitmap_image = QBitmap("assets/drawable/" + input_id + ".png")
        
        if self.bitmap_image == None:
            raise RuntimeError("Could not load image resource")

    def __init__(self, geo_coord, new_id, up_v=Vector3(0.0, 1.0, 0.0), im_scale=1):
        '''
        Constructor
        '''
        Source.__init__(self, colors.WHITE, geo_coord)
        self.image_scale = im_scale
        self.set_up_vector(up_v)
        self.set_image_id(new_id)
        self.requires_blending = False
        self.bitmap_image = None
    
        # horizontal corner
        self.ux = 0
        self.uy = 0
        self.uz = 0
        # vertical corner
        self.vx = 0
        self.vy = 0
        self.vz = 0
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''