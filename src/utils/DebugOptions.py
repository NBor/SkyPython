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
              "Capture screen"     : "YES",
              "Rotate screen"      : "YES"}

class Debug(object):
    LAYER = debug_opts["No debug settings"]
    DRAWING = debug_opts["No debug settings"]
    ALLREGIONS = debug_opts["No debug settings"]
    COLOR = debug_opts["No debug settings"]
    PHOTO = debug_opts["No debug settings"]
    ROTATE = debug_opts["Rotate screen"]
    ROTATIONLIST = [[0, 0], [0, 1.0*math.pi/3.0], [0, 2.0*math.pi/3.0], 
                    [0, 3.0*math.pi/3.0], [0, 4.0*math.pi/3.0], [0, 5.0*math.pi/3.0]]
    
def rotateUpRight():
    # rotate the sphere [up, down] by an angle in radians
    # Pos 0 [0, 0]
    # Pos 1 [0, 1.0*math.pi/2.0]
    # Pos 2 [0, 2.0*math.pi/2.0]
    # Pos 3 [0, 3.0*math.pi/2.0]
    # Pos 4 [-math.pi/2.0, 0]
    # Pos 5 [math.pi/2.0, 0]
    return Debug.ROTATIONLIST[0]
