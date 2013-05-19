'''
Created on 2013-05-19

@author: Neil
'''

def get_rowmatrix_from_vectors(v1, v2, v3):
    return Matrix33(v1.x, v1.x, v1.x, \
                    v2.y, v2.y, v2.y, \
                    v3.z, v3.z, v3.z)

def get_colmatrix_from_vectors(v1, v2, v3):
    return Matrix33(v1.x, v2.x, v3.x, \
                    v1.y, v2.y, v3.y, \
                    v1.z, v2.z, v3.z)
    
def get_identity_matrix():
    return Matrix33(1, 0, 0, 0, 1, 0, 0, 0, 1)

class Matrix33(object):
    '''
    classdocs
    '''
    xx = 0.0
    xy = 0.0
    xz = 0.0
    yx = 0.0
    yy = 0.0
    yz = 0.0
    zx = 0.0
    zy = 0.0
    zz = 0.0
    
    def clone(self):
        return Matrix33(self.xx, self.xy, self.xz, \
                        self.yx, self.yy, self.yz, \
                        self.zx, self.zy, self.zz)

    def get_determinant(self):
        return (self.xx * self.yy * self.zz) + \
            (self.xy * self.yz * self.zx) + \
            (self.xz * self.yx * self.zy) - \
            (self.xx * self.yz * self.zy) - \
            (self.yy * self.zx * self.xz) - \
            (self.zz * self.xy * self.yx)
            
    def get_inverse(self):
        det = self.get_determinant()
        if det == 0.0: return None
        return Matrix33( (self.yy * self.zz - self.yz * self.zy) / det, \
                         (self.xz * self.zy - self.xy * self.zz) / det, \
                         (self.xy * self.yz - self.xz * self.yy) / det, \
                         (self.yz * self.zx - self.yx * self.zz) / det, \
                         (self.xx * self.zz - self.xz * self.zx) / det, \
                         (self.xz * self.yx - self.xx * self.yz) / det, \
                         (self.yx * self.zy - self.yy * self.zx) / det, \
                         (self.xy * self.zx - self.xx * self.zy) / det, \
                         (self.xx * self.yy - self.xy * self.yx) / det)
        
    def transpose(self):
        tmp = self.xy
        self.xy = self.yx
        self.yx = tmp

        tmp = self.xz
        self.xz = self.zx
        self.zx = tmp

        tmp = self.yz
        self.yz = self.zy
        self.zy = tmp

    def __init__(self,  new_xx, new_xy, new_xz, \
                        new_yx, new_yy, new_yz, \
                        new_zx, new_zy, new_zz):
        '''
        Construct a new matrix.
        xx row 1, col 1
        xy row 1, col 2
        xz row 1, col 3
        yx row 2, col 1
        yy row 2, col 2
        yz row 2, col 3
        zx row 3, col 1
        zy row 3, col 2
        zz row 3, col 3
        '''
        self.xx = float(new_xx)
        self.xy = float(new_xy)
        self.xz = float(new_xz)
        self.yx = float(new_yx)
        self.yy = float(new_yy)
        self.yz = float(new_yz)
        self.zx = float(new_zx)
        self.zy = float(new_zy)
        self.zz = float(new_zz)
        
if __name__ == "__main__":
    '''
    for debugging purposes
    Ready for testing
    '''
    M = get_identity_matrix()
    print M.get_determinant()
    M2 = Matrix33(3, 0, 4, 0, 1, 0, 1, 2, 1)
    M2.transpose()
    print M2.xx, M2.xy, M2.xz
    print M2.yx, M2.yy, M2.yz
    print M2.zx, M2.zy, M2.zz