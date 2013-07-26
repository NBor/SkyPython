'''
Created on 2013-07-16

@author: Neil
'''

debug_opts = {"No debug settings"  : None,
              "View only stars"    : "STARS ONLY",
              "Stars, Const, Mess" : "FIRST 3",
              "View only points"   : "POINTS ONLY",
              "View points/lines"  : "POINTS AND LINES",
              "Draw all regions"   : "YES",
              "View white objects" : "WHITE ONLY",
              "Capture screen"     : "YES"}

class Debug(object):
    LAYER = debug_opts["Stars, Const, Mess"]
    DRAWING = debug_opts["View points/lines"]
    ALLREGIONS = debug_opts["Draw all regions"]
    COLOR = debug_opts["No debug settings"]
    RADIUSOFVIEW = 90.0
    LOOKDIRVECTORS = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0], [0.0, -1.0, 0.0]]
    UPDIRVECTORS = [[0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [0.0, 1.0, 0.0], [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    RIGHTVECTORS = [[0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0], [0.0, 0.0, 1.0], [0.0, 0.0, 1.0]]
    
