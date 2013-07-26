'''
Created on 2013-07-16

@author: Neil
'''

import math

debug_opts = {"No debug settings"  : None,
              "View only stars"    : "STARS ONLY",
              "Stars, Const, Mess" : "FIRST 3",
              "View only points"   : "POINTS ONLY",
              "Draw all regions"   : "YES",
              "View white objects" : "WHITE ONLY",
              "Capture screen"     : "YES"}

class Debug(object):
    LAYER = debug_opts["View only stars"]
    DRAWING = debug_opts["View only points"]
    ALLREGIONS = debug_opts["Draw all regions"]
    COLOR = debug_opts["View white objects"]
    RADIUSOFVIEW = 90.0
    LOOKDIRVECTORS = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0], [0.0, -1.0, 0.0]]
    UPDIRVECTORS = [[0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    RIGHTVECTORS = [[0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]
    
def rotateUpRight():
    # rotate the sphere [up, down] by an angle in radians
    # Pos 0 [0, 0]
    # Pos 1 [0, 1.0*math.pi/2.0]
    # Pos 2 [0, 2.0*math.pi/2.0]
    # Pos 3 [0, 3.0*math.pi/2.0]
    # Pos 4 [-math.pi/2.0, 0]
    # Pos 5 [math.pi/2.0, 0]
    return Debug.ROTATIONLIST[0]
