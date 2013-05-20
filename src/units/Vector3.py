'''
Created on 2013-05-16

@author: Neil
'''

import math

class Vector3(object):
    '''
    classdocs
    '''
    x = 0
    y = 0
    z = 0
    
    def assign(self, new_x=0, new_y=0, new_z=0, vector3=None):
        if vector3 != None:
            self.x = vector3.x
            self.y = vector3.y
            self.z = vector3.z
        else:
            self.x = float(new_x)
            self.y = float(new_y)
            self.z = float(new_z)
            
    def copy(self):
        return Vector3(self.x, self.y, self.z)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self):
        self.x = self.x / self.length()
        self.y = self.y / self.length()
        self.z = self.z / self.length()
        
    def scale(self, value):
        self.x = self.x * float(value)
        self.y = self.y * float(value)
        self.z = self.z * float(value)
        
    def to_float_array(self):
        return [self.x, self.y, self.z]
    
    def equals(self, v3_object):
        try:
            if v3_object.x == self.x and v3_object.y == self.y and v3_object.z == self.z:
                return True
            else:
                return False
        except:
            return False
    
    def hash_code(self):
        raise NotImplemented("hash code not implemented")
        
    def to_string(self):
        return "x={0}, y={1}, z={2}".format(self.x, self.y, self.z)

    def __init__(self, new_x=0, new_y=0, new_z=0, coord_list=None):
        '''
        Constructor
        '''
        if coord_list != None and len(coord_list) == 3:
            self.x = float(coord_list[0])
            self.y = float(coord_list[1])
            self.z = float(coord_list[2])
        else:
            self.x = float(new_x)
            self.y = float(new_y)
            self.z = float(new_z)
        
if __name__ == "__main__":
    '''
    For Debugging purposes
    Ready for testing
    '''
    A = Vector3(1, 2, 3)
    B = Vector3(9, 8, 7)
    A.assign(vector3=B)
    print A.x, A.y, A.z
    A.assign(2, 4, 4)
    print A.length() 
    print A.to_string()