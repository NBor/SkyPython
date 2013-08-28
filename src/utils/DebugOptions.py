'''
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


Created on 2013-07-16

@author: Neil Borle
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
    '''
    This class exists to make taking pictures of a subset of 
    objects easier at various location in the sky
    '''
    LAYER = debug_opts["No debug settings"]
    DRAWING = debug_opts["No debug settings"]
    ALLREGIONS = debug_opts["No debug settings"]
    COLOR = debug_opts["No debug settings"]
    RADIUSOFVIEW = 90.0
    LOOKDIRVECTORS = [[1.0, 0.0, 0.0], [0.0, 0.0, 1.0],  [-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0],  [0.0, -1.0, 0.0]]
    UPDIRVECTORS =   [[0.0, 1.0, 0.0], [0.0, 1.0, 0.0],  [0.0, 1.0, 0.0],  [0.0, 1.0, 0.0],  [-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
    RIGHTVECTORS =   [[0.0, 0.0, 1.0], [-1.0, 0.0, 0.0], [0.0, 0.0, -1.0], [1.0, 0.0, 0.0],  [0.0, 0.0, 1.0],  [0.0, 0.0, 1.0]]
    
