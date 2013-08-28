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
// Original Author: Kevin Serafini, Brent Bryan, Dominic Widdows, John Taylor
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


Created on 2013-05-17

@author: Neil Borle
'''
import math
from src.units.GeocentricCoordinates import GeocentricCoordinates
from src.units.Matrix33 import Matrix33
from src.units.Vector3 import Vector3
from TimeUtil import mean_sidereal_time

def degrees_to_radians(val):
    '''
    Convert degrees to radians
    '''
    return val * (math.pi / 180.0)

def radians_to_degrees(val):
    '''
    Convert radians to degrees
    '''
    return val * (180.0 / math.pi)

def abs_floor(x):
    '''
    returns Integer value
    '''
    if x >= 0.0:
        return math.floor(x)
    else:
        return math.ceil(x)

def mod_2_pi(x):
    '''
    Returns the modulo the given value by 2\pi. Returns an angle in the range 0
    to 2\pi radians.
    '''
    factor = x / (2 * math.pi)
    result = (2 * math.pi) * (factor - abs_floor(factor))
    if result < 0.0:
        return (2 * math.pi) + result
    else:
        return result

def scalar_product(v1, v2):
    '''
    given two vector3 objects perform the scalar product
    '''
    return (v1.x * v2.x) + (v1.y * v2.y) + (v1.z * v2.z)

def vector_product(v1, v2):
    '''
    given two vector3 objects perform the vector product
    '''
    term1 = v1.y * v2.z - v1.z * v2.y
    term2 = -v1.x * v2.z + v1.z * v2.x
    term3 = v1.x * v2.y - v1.y * v2.x
    return Vector3(term1, term2, term3)

def scale_vector(v3, scale):
    '''
    return new scaled vector
    '''
    return Vector3(scale * v3.x, scale * v3.y, scale * v3.z)

def add_vectors(v1, v2):
    '''
    return a new vector whos coordinates are the sum of the 
    two input vectors
    '''
    return Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def cosine_similarity(v1, v2):
    '''
    perform cosine similarity
    '''
    demoninator = math.sqrt(scalar_product(v1, v1) * scalar_product(v2, v2))
    return scalar_product(v1, v2) / demoninator

def getXYZ(ra_dec):
    '''
    Convert ra and dec to x,y,z where the point is place on the unit sphere.
    '''
    ra_radians = degrees_to_radians(ra_dec.ra)
    dec_radians = degrees_to_radians(ra_dec.dec)
    x = math.cos(ra_radians) * math.cos(dec_radians)
    y = math.sin(ra_radians) * math.cos(dec_radians)
    z = math.sin(dec_radians)
    return GeocentricCoordinates(x, y, z)
    
def calculate_RADec_of_zenith(date_utc, lat_long_location):
    '''
    compute coordinates of the zenith
    date_utc must be a time.gmtime() struct
    '''
    my_ra = mean_sidereal_time(date_utc, lat_long_location.longitude)
    my_dec = lat_long_location.latitude
    return my_ra, my_dec

def matrix_multiply(m1, m2):
    '''
    multiply m1 * m2 and return a new matrix
    '''
    return Matrix33(m1.xx*m2.xx + m1.xy*m2.yx + m1.xz*m2.zx,
                    m1.xx*m2.xy + m1.xy*m2.yy + m1.xz*m2.zy,
                    m1.xx*m2.xz + m1.xy*m2.yz + m1.xz*m2.zz,
                    m1.yx*m2.xx + m1.yy*m2.yx + m1.yz*m2.zx,
                    m1.yx*m2.xy + m1.yy*m2.yy + m1.yz*m2.zy,
                    m1.yx*m2.xz + m1.yy*m2.yz + m1.yz*m2.zz,
                    m1.zx*m2.xx + m1.zy*m2.yx + m1.zz*m2.zx,
                    m1.zx*m2.xy + m1.zy*m2.yy + m1.zz*m2.zy,
                    m1.zx*m2.xz + m1.zy*m2.yz + m1.zz*m2.zz)
    
def matrix_vector_multiply(m, v):
    '''
    multiply m * v where m is a matrix and v is a vector
    '''
    return Vector3(m.xx*v.x + m.xy*v.y + m.xz*v.z,
                    m.yx*v.x + m.yy*v.y + m.yz*v.z,
                    m.zx*v.x + m.zy*v.y + m.zz*v.z)

def calculate_rotation_matrix(degrees, axis):
    '''
    Calculate the rotation matrix for a certain number of degrees about the
    give axis. Vector3 axis input must be a unit vector.
    '''
    cos_d = math.cos(degrees_to_radians(degrees))
    sin_d = math.sin(degrees_to_radians(degrees))
    one_minus_cos_d = 1.0 - cos_d
    
    xs = axis.x * sin_d
    ys = axis.y * sin_d
    zs = axis.z * sin_d
    
    xm = axis.x * one_minus_cos_d;
    ym = axis.y * one_minus_cos_d;
    zm = axis.z * one_minus_cos_d;
 
    xym = axis.x * ym;
    yzm = axis.y * zm;
    zxm = axis.z * xm;
    
    return Matrix33(axis.x * xm + cos_d, xym + zs, zxm - ys,
                    xym - zs, axis.y * ym + cos_d, yzm + xs,
                    zxm + ys, yzm - xs, axis.z * zm + cos_d)

if __name__ == "__main__":
    '''
    For debugging purposes
    '''
    import time
    import units.LatLong as LL
    from units.RaDec import RaDec
    
    M = calculate_rotation_matrix(90, Vector3(1, 0, 0))
    print M.xx, M.xy, M.xz
    print M.yx, M.yy, M.yz
    print M.zx, M.zy, M.zz
    ra, dec = calculate_RADec_of_zenith(time.gmtime(), LL.LatLong(20, 16))
    radec = RaDec(ra, dec)
    print radec.ra, radec.dec
    