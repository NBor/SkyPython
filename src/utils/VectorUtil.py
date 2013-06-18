'''
Created on 2013-05-20

@author: Neil
'''

import math
from units.Vector3 import Vector3

def zero():
    return Vector3(0, 0, 0)

def dot_product(p1, p2):
    return float(p1.x * p2.x + p1.y * p2.y + p1.z * p2.z)

def cross_product(p1, p2):
    return Vector3(p1.y * p2.z - p1.z * p2.y,
                   -p1.x * p2.z + p1.z * p2.x,
                   p1.x * p2.y - p1.y * p2.x)
    
def angle_between(p1, p2):
    return math.acos(dot_product(p1, p2) / float((length(p1) * length(p2))))

def length(v):
    return math.sqrt(dot_product(v, v));

def normalized(v):
    length_of_V = length(v);
    if length_of_V < 0.000001:
        return zero()
    else:
        return scale(v, (1.0 / float(length_of_V)))
    
def project(v, onto):
    return scale(float(dot_product(v, onto) / length(onto)), onto)

def project_onto_unit(v, onto):
    return scale(dot_product(v, onto), onto)

def project_onto_plane(v, unit_normal):
    return difference(v, project_onto_unit(v, unit_normal))

def negate(v):
    return Vector3(-v.x, -v.y, -v.z)

def sum_vectors(v1, v2):
    return Vector3(v1.x + v2.x, v1.y + v2.y, v1.z + v2.z)

def difference(v1, v2):
    return sum_vectors(v1, negate(v2))

def scale(v, factor):
    return Vector3(v.x * factor, v.y * factor, v.z * factor)
    
if __name__ == "__main__":
    '''
    For debugging purposes
    Ready for testing
    '''
    