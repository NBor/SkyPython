'''
Created on 2013-05-16

@author: Neil
'''

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
    requires_blending = False
    bitmap_image = None
    
    # horizontal corner
    ux = 0
    uy = 0
    uz = 0
    # vertical corner
    vx = 0
    vy = 0
    vz = 0

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
    
    def set_image_by_id(self, input_id):
        self.bitmap_image = input_id
        raise NotImplemented("this has not been done yet")

    def __init__(self, geo_coord, new_id, up_v=Vector3(0.0, 1.0, 0.0), im_scale=1):
        '''
        Constructor
        '''
        Source.__init__(self, colors.WHITE, geo_coord)
        self.image_scale = im_scale
        self.set_up_vector(up_v)
        self.set_image_by_id(new_id)
        
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''