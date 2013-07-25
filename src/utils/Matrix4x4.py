'''
Created on 2013-05-26

@author: Neil
'''

import math
from ..units.Vector3 import Vector3

def create_identity():
    return create_scaling(1, 1, 1)
    
def create_scaling(x, y, z):
    return Matrix4x4([float(x), 0, 0, 0,
                      0, float(y), 0, 0,
                      0, 0, float(z), 0,
                      0, 0, 0, 1])
        
def create_translation(x, y, z):
    return Matrix4x4([1, 0, 0, 0,
                      0, 1, 0, 0,
                      0, 0, 1, 0,
                      float(x), float(y), float(z), 1])
        
def create_rotation(angle, vector3):
    m = [0.0] *16
    x_sqr = vector3.x * vector3.x
    y_sqr = vector3.y * vector3.y
    z_sqr = vector3.z * vector3.z
    
    sin_angle = math.sin(angle)
    
    cos_angle = math.cos(angle)
    one_minus_cos_angle = 1.0 - cos_angle
    
    x_sin_angle = vector3.x * sin_angle
    y_sin_angle = vector3.y * sin_angle
    z_sin_angle = vector3.z * sin_angle
    
    z_one_minus_cos_angle = vector3.z * one_minus_cos_angle
    
    xy_one_minus_cos_angle = vector3.x * vector3.y * one_minus_cos_angle
    xz_one_minus_cos_angle = vector3.x * z_one_minus_cos_angle
    yz_one_minus_cos_angle = vector3.y * z_one_minus_cos_angle
    m[0] = x_sqr + (y_sqr + z_sqr) * cos_angle
    m[1] = xy_one_minus_cos_angle + z_sin_angle
    m[2] = xz_one_minus_cos_angle - y_sin_angle
    m[3] = 0
    
    m[4] = xy_one_minus_cos_angle - z_sin_angle
    m[5] = y_sqr + (x_sqr + z_sqr) * cos_angle
    m[6] = yz_one_minus_cos_angle + x_sin_angle
    m[7] = 0
    
    m[8] = xz_one_minus_cos_angle + y_sin_angle
    m[9] = yz_one_minus_cos_angle - x_sin_angle
    m[10] = z_sqr + (x_sqr + y_sqr) * cos_angle
    m[11] = 0
    
    m[12] = 0
    m[13] = 0
    m[14] = 0
    m[15] = 1
    
    return Matrix4x4(m)
    
def create_perspective_projection(width, height, fovy_in_radians):
    near = 0.01
    far = 10000.0
    
    inverse_aspect_ratio = height / float(width)
    
    one_over_tan_half_radius_of_view = 1.0 / math.tan(fovy_in_radians)
    
    return Matrix4x4([
        inverse_aspect_ratio * one_over_tan_half_radius_of_view, 0, 0, 0,
        0, one_over_tan_half_radius_of_view, 0, 0, 
        0, 0, -(far + near) / float(far - near), -1,
        0, 0, -2.0*far*near / float(far - near), 0])

def create_view(look_dir, up, right):
    return Matrix4x4([ \
        right.x,
        up.x,
        -look_dir.x,
        0,
    
        right.y,
        up.y,
        -look_dir.y,
        0,
    
        right.z,
        up.z,
        -look_dir.z,
        0,
    
        0,
        0,
        0,
        1])
        
def multiply_MM(mat1, mat2):
    m = mat1.values[:]
    n = mat2.values[:]
    
    return Matrix4x4([ \
        m[0]*n[0] + m[4]*n[1] + m[8]*n[2] + m[12]*n[3],
        m[1]*n[0] + m[5]*n[1] + m[9]*n[2] + m[13]*n[3],
        m[2]*n[0] + m[6]*n[1] + m[10]*n[2] + m[14]*n[3],
        m[3]*n[0] + m[7]*n[1] + m[11]*n[2] + m[15]*n[3],
    
        m[0]*n[4] + m[4]*n[5] + m[8]*n[6] + m[12]*n[7],
        m[1]*n[4] + m[5]*n[5] + m[9]*n[6] + m[13]*n[7],
        m[2]*n[4] + m[6]*n[5] + m[10]*n[6] + m[14]*n[7],
        m[3]*n[4] + m[7]*n[5] + m[11]*n[6] + m[15]*n[7],
    
        m[0]*n[8] + m[4]*n[9] + m[8]*n[10] + m[12]*n[11],
        m[1]*n[8] + m[5]*n[9] + m[9]*n[10] + m[13]*n[11],
        m[2]*n[8] + m[6]*n[9] + m[10]*n[10] + m[14]*n[11],
        m[3]*n[8] + m[7]*n[9] + m[11]*n[10] + m[15]*n[11],
    
        m[0]*n[12] + m[4]*n[13] + m[8]*n[14] + m[12]*n[15],
        m[1]*n[12] + m[5]*n[13] + m[9]*n[14] + m[13]*n[15],
        m[2]*n[12] + m[6]*n[13] + m[10]*n[14] + m[14]*n[15],
        m[3]*n[12] + m[7]*n[13] + m[11]*n[14] + m[15]*n[15]])
        
def multiply_MV(mat, v):
    m = mat.values[:]
    return Vector3(
        m[0]*v.x + m[4]*v.y + m[8]*v.z + m[12],
        m[1]*v.x + m[5]*v.y + m[9]*v.z + m[13],
        m[2]*v.x + m[6]*v.y + m[10]*v.z + m[14])
        
def transform_vector(mat, v):
    trans = multiply_MV(mat, v)
    m = mat.values[:]
    w = m[3]*v.x + m[7]*v.y + m[11]*v.z + m[15]
    one_over_w = 1.0 / float(w)
    trans.x *= one_over_w
    trans.y *= one_over_w
    # Don't transform z, we just leave it as a "pseudo-depth".
    return trans

class Matrix4x4(object):
    '''
    classdocs
    '''
    values = [0.0] * 16

    def __init__(self, contents):
        '''
        Constructor
        '''
        if len(contents) == 16:
            self.values = [float(x) for x in contents]
        else:
            raise IndexError("input not of len 16")