'''
// Copyright 2008 Google Inc.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
// 
// Original Author: Not stated
// 
// Notification of Change: The original java source code has been
// modified in that it has been rewritten in the python programming
// language and additionally, may contain components and ideas that are 
// not found in the original source code.


   Copyright 2013 Neil Borle and Paul Lu

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.


Created on 2013-05-16

@author: Neil Borle
'''

import math

class Vector3(object):
    '''
    Basic Vector class in 3 dimensions. It is inherited by
    [Geo/Helio]centric coordinates
    '''
    def assign(self, new_x=0.0, new_y=0.0, new_z=0.0, vector3=None):
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
        norm = self.length()
        self.x = self.x / norm
        self.y = self.y / norm
        self.z = self.z / norm
        
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

    def __init__(self, new_x=0.0, new_y=0.0, new_z=0.0, coord_list=None):
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
    '''
    A = Vector3(1, 2, 3)
    B = Vector3(9, 8, 7)
    A.assign(vector3=B)
    print A.x, A.y, A.z
    A.assign(2, 4, 4)
    print A.length() 
    print A.to_string()